# The PostgreSQL database (RDS), the app's data store. It lives in the PRIVATE subnets
# (no internet route), accepts connections only from the app via the `db` security
# group, and lets RDS generate and store its own master password in Secrets Manager.
#
# This is the FIRST resource that costs money: db.t4g.small is ~$25-30/mo while running.
# "Destroy when idle" is how we keep the bill near zero between demos.

# A Terraform-generated master password. Alphanumeric only (special = false) so it never
# contains characters like '#' or '[' that break connection URLs or shell quoting. It's
# stored in Terraform state (which lives in the encrypted S3 bucket).
resource "random_password" "db" {
  length  = 30
  special = false
}

# Tells RDS which subnets it may place the database in: the private ones, across 2 AZs
# (RDS requires at least two, even for a single-AZ instance).
resource "aws_db_subnet_group" "main" {
  name       = "${var.project}-db"
  subnet_ids = module.vpc.private_subnets
  tags       = { Name = "${var.project}-db" }
}

resource "aws_db_instance" "main" {
  identifier = "${var.project}-db"

  engine         = "postgres"
  engine_version = "16"           # latest 16.x minor; ships pgvector with HNSW support
  instance_class = "db.t4g.small" # 2 vCPU burstable, 2 GB RAM, ARM Graviton (cheap)

  # Storage: the corpus is ~1-2 GB (embeddings + HNSW index); 20 GB gp3 is plenty.
  allocated_storage = 20
  storage_type      = "gp3"
  storage_encrypted = true

  db_name  = "bdr" # the initial database the app connects to
  username = "bdr" # master username

  # Master password we generate ourselves (see random_password.db above). Reliable and
  # URL/shell-safe, unlike the RDS-managed password we started with.
  password = random_password.db.result

  # Network placement: private subnets, the db security group, never reachable publicly.
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db.id]
  publicly_accessible    = false
  multi_az               = false # single-AZ to save cost (this is a demo)

  # Demo lifecycle: the data is reloaded from an S3 dump, so the database is disposable.
  # These settings let `terraform destroy` finish quickly and cheaply.
  backup_retention_period = 0     # no automated backups (data comes from S3)
  skip_final_snapshot     = true  # don't snapshot on destroy
  deletion_protection     = false # allow destroy
  apply_immediately       = true
}

output "db_endpoint" {
  value       = aws_db_instance.main.address
  description = "RDS endpoint hostname (the host part of DATABASE_URL)."
}

output "db_password" {
  value       = random_password.db.result
  sensitive   = true
  description = "Master DB password. Fetch with: terraform output -raw db_password"
}
