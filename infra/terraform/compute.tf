# Compute layer: the registry (ECR) plus the ECS/Fargate service that runs the app
# container behind an Application Load Balancer (ALB).
#
# Once it's all up, the request path is:
#   internet --(HTTP :80)--> ALB --(:8000)--> Fargate task (the FastAPI container)
#
# HTTPS and the custom domain are added later (the edge step). For now we reach the app
# over plain HTTP at the ALB's AWS-provided DNS name.

# ===========================================================================
# ECR: the private image registry
# ===========================================================================
resource "aws_ecr_repository" "app" {
  name = var.project

  # MUTABLE = a tag like :latest can be overwritten (fine for a demo; prod often pins
  # IMMUTABLE + unique tags per build).
  image_tag_mutability = "MUTABLE"

  force_delete = true # let `terraform destroy` remove the repo even if it holds images

  image_scanning_configuration {
    scan_on_push = true # free basic vulnerability scan on each push
  }
}

output "ecr_repository_url" {
  value       = aws_ecr_repository.app.repository_url
  description = "The image registry URL to build and push the app image to."
}

# ===========================================================================
# Logs: where the container's output goes
# ===========================================================================
resource "aws_cloudwatch_log_group" "app" {
  name              = "/ecs/${var.project}"
  retention_in_days = 14
}

# ===========================================================================
# IAM: the role ECS uses to START the container
# ===========================================================================
# The "execution role" is what ECS itself assumes to set the task up: pull the image
# from ECR, fetch the secrets we inject, and write logs. (This is separate from the
# app's own runtime permissions, which it doesn't need any of.)

# Who is allowed to assume this role: the ECS tasks service.
data "aws_iam_policy_document" "ecs_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "task_execution" {
  name               = "${var.project}-task-execution"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json
}

# AWS's standard managed policy for this role (ECR pull + CloudWatch logs).
resource "aws_iam_role_policy_attachment" "task_execution" {
  role       = aws_iam_role.task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Plus permission to read the specific app secrets we inject into the container.
data "aws_iam_policy_document" "read_secrets" {
  statement {
    actions = ["secretsmanager:GetSecretValue"]
    resources = concat(
      [for s in aws_secretsmanager_secret.app : s.arn],
      [aws_secretsmanager_secret.db_password.arn],
    )
  }
}

resource "aws_iam_role_policy" "read_secrets" {
  name   = "read-app-secrets"
  role   = aws_iam_role.task_execution.id
  policy = data.aws_iam_policy_document.read_secrets.json
}

# ===========================================================================
# ECS cluster + task definition (the blueprint of what to run)
# ===========================================================================
resource "aws_ecs_cluster" "main" {
  name = var.project
}

resource "aws_ecs_task_definition" "app" {
  family                   = var.project
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 512  # 0.5 vCPU
  memory                   = 1024 # 1 GB
  execution_role_arn       = aws_iam_role.task_execution.arn

  # Match the ARM64 image we pushed (and the Graviton database) -> cheaper compute.
  runtime_platform {
    cpu_architecture        = "ARM64"
    operating_system_family = "LINUX"
  }

  # The container blueprint, as JSON.
  container_definitions = jsonencode([
    {
      name         = "app"
      image        = "${aws_ecr_repository.app.repository_url}:latest"
      essential    = true
      portMappings = [{ containerPort = var.app_port }]

      # Plain (non-secret) settings, including how to reach the database (everything
      # except the password, which is a secret below).
      environment = [
        { name = "RETRIEVAL_BACKEND", value = "pgvector" },
        { name = "FRONTEND_ORIGIN", value = "https://${var.domain}" },
        { name = "DAILY_SPEND_CAP_USD", value = "5" },
        { name = "OWNER_SPEND_CAP_USD", value = "25" },
        { name = "DB_HOST", value = aws_db_instance.main.address },
        { name = "DB_NAME", value = "bdr" },
        { name = "DB_USER", value = "bdr" },
      ]

      # Secret settings, injected from Secrets Manager at start (never baked into the
      # image): the OpenAI key and the database password.
      secrets = [
        { name = "OPENAI_API_KEY", valueFrom = aws_secretsmanager_secret.app["openai_api_key"].arn },
        { name = "DB_PASSWORD", valueFrom = aws_secretsmanager_secret.db_password.arn },
        { name = "ACCESS_CODE", valueFrom = aws_secretsmanager_secret.app["access_code"].arn },
        { name = "OWNER_CODE", valueFrom = aws_secretsmanager_secret.app["owner_code"].arn },
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.app.name
          "awslogs-region"        = var.region
          "awslogs-stream-prefix" = "app"
        }
      }
    }
  ])
}

# ===========================================================================
# Application Load Balancer: the public entry point
# ===========================================================================
resource "aws_lb" "main" {
  name               = "${var.project}-alb"
  load_balancer_type = "application"
  internal           = false
  subnets            = module.vpc.public_subnets
  security_groups    = [aws_security_group.alb.id]

  # Hold streaming (SSE) connections open through the quiet synthesis gap.
  idle_timeout = 150
}

# The ALB forwards matching requests into this group; its targets are the Fargate tasks.
resource "aws_lb_target_group" "app" {
  name        = "${var.project}-tg"
  port        = var.app_port
  protocol    = "HTTP"
  vpc_id      = module.vpc.vpc_id
  target_type = "ip" # Fargate (awsvpc networking) registers tasks by IP, not instance

  health_check {
    path                = "/health"
    matcher             = "200"
    interval            = 15 # check every 15s (default is 30)
    timeout             = 5
    healthy_threshold   = 2 # mark healthy after 2 passes (~30s) -> faster deploys/failover
    unhealthy_threshold = 3 # tolerate a couple of blips before replacing a task
  }
}

# Listen on port 80 (HTTP) and forward to the app. HTTPS (443) is added in the edge step.
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

# ===========================================================================
# ECS service: run the task, register it with the load balancer, keep it running
# ===========================================================================
resource "aws_ecs_service" "app" {
  name            = var.project
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  # Zero-downtime rolling deploys: keep 100% healthy while bringing up to 200%.
  deployment_minimum_healthy_percent = 100
  deployment_maximum_percent         = 200

  # Give a freshly-started task time to boot before health checks may replace it.
  health_check_grace_period_seconds = 60

  network_configuration {
    subnets          = module.vpc.public_subnets
    security_groups  = [aws_security_group.task.id]
    assign_public_ip = true # public subnet + public IP -> reaches OpenAI via IGW (no NAT)
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "app"
    container_port   = var.app_port
  }

  depends_on = [aws_lb_listener.http]

  # CI/CD deploys new task-definition revisions (image tagged by git SHA). Ignore the
  # task_definition here so Terraform doesn't revert the service to its own revision on the
  # next apply. (Terraform still owns the task-def template; CI picks up env/secret changes
  # the next time it renders + deploys.)
  lifecycle {
    ignore_changes = [task_definition]
  }
}

output "alb_dns_name" {
  value       = aws_lb.main.dns_name
  description = "Public DNS name of the load balancer (reach the app here over HTTP for now)."
}
