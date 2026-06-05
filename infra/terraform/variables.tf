# Input variables: reusable settings referenced elsewhere as `var.<name>`. Defining
# them here (with defaults) means we set a value once and reuse it across files.

variable "region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region for all resources. us-east-1 keeps the CloudFront certificate in-region."
}

variable "project" {
  type        = string
  default     = "bdr"
  description = "Short prefix used when naming resources (e.g. bdr-vpc, bdr-db)."
}

variable "app_port" {
  type        = number
  default     = 8000
  description = "Port the FastAPI container listens on (matches the Dockerfile)."
}

variable "domain" {
  type        = string
  default     = "answertrail.yeesengchan.com"
  description = "Delegated subdomain. Frontend at the apex; API at api.<domain>."
}
