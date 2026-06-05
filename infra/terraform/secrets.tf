# Secrets Manager holds the sensitive values the app reads at runtime. We create the
# secret "containers" here but NOT their values: you set those out-of-band (console or
# CLI), so secrets never live in Terraform code, state, or git. The ECS task will read
# them by ARN when the container starts.
#
# (The database password is NOT here: RDS manages its own master-password secret, see
# data.tf. These are the app's other secrets.)
#
# recovery_window_in_days = 0 lets `terraform destroy` delete them immediately, so a
# destroy/apply cycle can recreate the same names without hitting Secrets Manager's
# default 7-30 day "scheduled for deletion" waiting period.

locals {
  app_secret_names = [
    "openai_api_key",
    "langfuse_public_key",
    "langfuse_secret_key",
    "access_code",
    "owner_code",
  ]
}

resource "aws_secretsmanager_secret" "app" {
  for_each                = toset(local.app_secret_names)
  name                    = "${var.project}/${each.value}"
  description             = "bounded-deep-research: ${each.value}"
  recovery_window_in_days = 0
}

output "app_secret_arns" {
  value       = { for k, s in aws_secretsmanager_secret.app : k => s.arn }
  description = "ARNs of the app secrets. Set their VALUES out-of-band before deploying ECS."
}

# The database password. Unlike the secrets above, Terraform DOES set this value, because
# it generated the password (random_password.db in data.tf). The task injects it as
# DB_PASSWORD so the password is never a plain environment variable.
resource "aws_secretsmanager_secret" "db_password" {
  name                    = "${var.project}/db_password"
  description             = "bounded-deep-research: database password"
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = random_password.db.result
}
