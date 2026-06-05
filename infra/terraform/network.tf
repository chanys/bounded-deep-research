# The app's private network on AWS: a VPC (your own isolated slice of the cloud) with
# public and private subnets across two Availability Zones.
#
# Layout:
#   - public subnets:  internet-facing things -> the load balancer + the app container
#     (which gets a public IP and reaches the internet directly via the Internet Gateway).
#   - private subnets: the database (RDS), reachable only from inside the VPC.
#   - two Availability Zones (separate data centers) because RDS requires subnets in >= 2.
#   - NO NAT gateway (deliberate): a NAT lets private subnets reach the internet outbound
#     and costs ~$32/mo. We don't need it here: the DB needs no outbound internet, and the
#     app lives in a public subnet, so it reaches the internet via the Internet Gateway.
#
# We use the community VPC module (proven, handles subnets/route-tables/gateway wiring)
# rather than hand-writing each resource.

# Ask AWS which Availability Zones exist in this region, so we don't hardcode names.
data "aws_availability_zones" "available" {
  state = "available"
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.project}-vpc"
  cidr = "10.0.0.0/16" # the VPC's private IP range (~65k addresses)

  # Use the first two available AZs in the region.
  azs = slice(data.aws_availability_zones.available.names, 0, 2)

  # IP ranges carved out of the VPC above (~256 addresses each).
  public_subnets  = ["10.0.0.0/24", "10.0.1.0/24"]   # internet-facing (ALB + app)
  private_subnets = ["10.0.10.0/24", "10.0.11.0/24"] # internal only (RDS)

  enable_nat_gateway = false # deliberately off (see header note)

  # Give resources DNS names and resolution inside the VPC (needed by the public app + ALB).
  enable_dns_hostnames = true
  enable_dns_support   = true
}
