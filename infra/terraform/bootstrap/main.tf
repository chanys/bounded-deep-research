# Bootstrap: create the S3 bucket that will hold Terraform's "state" for the rest of
# the project. This is a one-time setup, run before any other Terraform here.
#
# Why this is its own separate config: the main Terraform will store its state IN this
# bucket. But the bucket has to exist before it can be used for storage. So this small
# config creates the bucket using LOCAL state (a file on your machine), breaking the
# chicken-and-egg. After this runs once, you rarely touch it again.
#
# ---------------------------------------------------------------------------
# How to read the `resource` blocks below:
#
#     resource "aws_s3_bucket" "state" { ... }
#              \______________/  \_____/
#               (1) the TYPE      (2) a local NAME we pick
#
#   (1) TYPE  = what kind of AWS thing this is (here, an S3 bucket). Fixed name,
#               defined by the AWS provider.
#   (2) NAME  = a nickname WE choose, used only to refer to this thing elsewhere
#               in this file. It is NOT the name AWS sees. We reuse "state" for all
#               four blocks because they all concern the single state bucket.
#
#   To point one resource at another we write TYPE.NAME.ATTRIBUTE. For example
#   `aws_s3_bucket.state.id` means "the id (the bucket name) of the bucket declared
#   in the `aws_s3_bucket` `state` block".
#
#   IMPORTANT: in the AWS provider, a bucket and its settings are SEPARATE resources.
#   Only the first block (`aws_s3_bucket.state`) creates a bucket. The other three
#   each ATTACH one setting to that same bucket by pointing `bucket = ...` at it.
#   So there are four blocks below, but only ONE real bucket.
# ---------------------------------------------------------------------------

terraform {
  required_version = ">= 1.10"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
  # No `backend` block here on purpose: bootstrap uses local state, because it's
  # creating the very bucket a remote backend would need.
}

provider "aws" {
  region = var.region
}

variable "region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region for the state bucket."
}

# Look up the current AWS account id, used to make the bucket name globally unique.
data "aws_caller_identity" "current" {}

locals {
  # S3 bucket names must be unique across ALL of AWS, so we suffix with the account id.
  state_bucket = "bdr-terraform-state-${data.aws_caller_identity.current.account_id}"
}

# (1) THE BUCKET. This is the only block that actually creates a bucket.
# `bucket = <name>` here means "create a bucket with this name".
resource "aws_s3_bucket" "state" {
  bucket = local.state_bucket
}

# (2) A SETTING on the bucket above: turn on versioning (keep every past copy of the
# state file, so a bad apply can be rolled back). This does NOT create a bucket;
# `bucket = aws_s3_bucket.state.id` means "apply this setting to the bucket from (1)".
resource "aws_s3_bucket_versioning" "state" {
  bucket = aws_s3_bucket.state.id
  versioning_configuration {
    status = "Enabled"
  }
}

# (3) A SETTING on the same bucket: encrypt its contents at rest (the state file can
# contain sensitive values like the DB password). Again, not a new bucket, this
# attaches encryption to the bucket from (1). "AES256" is S3's built-in encryption.
resource "aws_s3_bucket_server_side_encryption_configuration" "state" {
  bucket = aws_s3_bucket.state.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# (4) A SETTING on the same bucket: make sure it can never be made public. Four flags,
# all true, slam every public-access door shut. Not a new bucket; a guard on (1).
resource "aws_s3_bucket_public_access_block" "state" {
  bucket                  = aws_s3_bucket.state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# After apply, print the bucket name. The main config's backend will point at it.
output "state_bucket" {
  value       = aws_s3_bucket.state.id
  description = "Name of the S3 bucket holding Terraform state."
}
