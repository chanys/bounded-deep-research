# Root Terraform config for the project's AWS infrastructure. Everything except the
# one-time state bucket (see ./bootstrap) is defined here and in the sibling .tf files
# (variables.tf, network.tf, etc.). You run `terraform` from THIS directory.

terraform {
  required_version = ">= 1.10"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
  }

  # THE BACKEND = where Terraform stores its "state" (its record of what it created).
  # We point it at the S3 bucket that ./bootstrap created, instead of a local file, so
  # the state is durable, encrypted, and lockable. Note: a backend block can't use
  # variables, so the bucket name is written out literally here.
  backend "s3" {
    bucket       = "bdr-terraform-state-841798536002"
    key          = "infra/terraform.tfstate" # the state file's path inside the bucket
    region       = "us-east-1"
    encrypt      = true # encrypt the state object at rest
    use_lockfile = true # S3-native locking (no separate DynamoDB table needed)
  }
}

# The AWS provider tells Terraform which account/region to act in. It reads your AWS
# CLI credentials automatically. `default_tags` stamps every resource we create with
# these tags, so the account never again looks like the untagged mess we cleaned up.
provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Project   = "bounded-deep-research"
      ManagedBy = "terraform"
      Env       = "prod"
    }
  }
}
