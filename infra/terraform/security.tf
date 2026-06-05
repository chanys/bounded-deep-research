# Security groups = stateful firewalls attached to resources. Three of them, layered so
# each tier only accepts traffic from the tier in front of it:
#
#     internet --443--> ALB --8000--> app task --5432--> database
#
# The only thing open to the whole internet is the ALB on 443. The rules below reference
# OTHER security groups (not IP ranges), which is how we say "only the app may reach the
# DB" without hardcoding any addresses.
#
# "Stateful" means: if an inbound connection is allowed, its reply is automatically
# allowed back out. That's why the database needs no egress rule, replies to the app's
# query flow back without one.

# ===========================================================================
# ALB security group: the only public door
# ===========================================================================
resource "aws_security_group" "alb" {
  name        = "${var.project}-alb"
  description = "ALB: allow HTTPS from the internet"
  vpc_id      = module.vpc.vpc_id
  tags        = { Name = "${var.project}-alb" }
}

resource "aws_vpc_security_group_ingress_rule" "alb_https" {
  security_group_id = aws_security_group.alb.id
  description       = "HTTPS from anyone"
  ip_protocol       = "tcp"
  from_port         = 443
  to_port           = 443
  cidr_ipv4         = "0.0.0.0/0" # the whole internet
}

# HTTP. Needed now because we serve over plain HTTP before TLS exists; later, port 80
# stays open to redirect http -> https.
resource "aws_vpc_security_group_ingress_rule" "alb_http" {
  security_group_id = aws_security_group.alb.id
  description       = "HTTP from anyone"
  ip_protocol       = "tcp"
  from_port         = 80
  to_port           = 80
  cidr_ipv4         = "0.0.0.0/0"
}

# The ALB must be able to forward requests onward to the app task.
resource "aws_vpc_security_group_egress_rule" "alb_all" {
  security_group_id = aws_security_group.alb.id
  description       = "All outbound (to the app task)"
  ip_protocol       = "-1" # -1 = any protocol/port
  cidr_ipv4         = "0.0.0.0/0"
}

# ===========================================================================
# App task security group: reachable only from the ALB
# ===========================================================================
resource "aws_security_group" "task" {
  name        = "${var.project}-task"
  description = "App task: inbound only from the ALB"
  vpc_id      = module.vpc.vpc_id
  tags        = { Name = "${var.project}-task" }
}

# The key rule: the app port accepts traffic ONLY from the ALB's security group,
# never directly from the internet (even though the task sits in a public subnet).
resource "aws_vpc_security_group_ingress_rule" "task_from_alb" {
  security_group_id            = aws_security_group.task.id
  description                  = "App port, from the ALB security group only"
  ip_protocol                  = "tcp"
  from_port                    = var.app_port
  to_port                      = var.app_port
  referenced_security_group_id = aws_security_group.alb.id
}

# The app needs outbound to the internet (OpenAI, whose IPs rotate, so we can't pin a
# destination) and to the database. Strictness lives on inbound, not outbound.
resource "aws_vpc_security_group_egress_rule" "task_all" {
  security_group_id = aws_security_group.task.id
  description       = "All outbound (OpenAI, database, etc.)"
  ip_protocol       = "-1"
  cidr_ipv4         = "0.0.0.0/0"
}

# ===========================================================================
# Database security group: reachable only from the app task
# ===========================================================================
resource "aws_security_group" "db" {
  name        = "${var.project}-db"
  description = "RDS: Postgres inbound only from the app task"
  vpc_id      = module.vpc.vpc_id
  tags        = { Name = "${var.project}-db" }
}

# Postgres (5432) accepted ONLY from the app task's security group. Nothing else in the
# VPC, and nothing on the internet, can reach the database. No egress rule needed
# (stateful: query replies flow back automatically; the DB never initiates connections).
resource "aws_vpc_security_group_ingress_rule" "db_from_task" {
  security_group_id            = aws_security_group.db.id
  description                  = "Postgres, from the app task security group only"
  ip_protocol                  = "tcp"
  from_port                    = 5432
  to_port                      = 5432
  referenced_security_group_id = aws_security_group.task.id
}
