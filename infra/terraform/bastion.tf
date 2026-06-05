# A tiny "bastion" host used ONLY to load data into the private database. It sits in a
# public subnet and relays a connection from your laptop (over AWS Session Manager, no
# SSH, no inbound ports) to RDS on the internal network. This is how we reach the private
# DB for admin tasks without ever making RDS publicly accessible.
#
# It's a t4g.nano (~$3/mo) and is torn down with everything else on `terraform destroy`.

# Latest Amazon Linux 2023 (ARM64) AMI, via AWS's published SSM parameter (so we don't
# hardcode an AMI id that goes stale).
data "aws_ssm_parameter" "al2023_arm" {
  name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-arm64"
}

# Role letting Session Manager manage the instance. No SSH key, no inbound rules needed.
data "aws_iam_policy_document" "ec2_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "bastion" {
  name               = "${var.project}-bastion"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume.json
}

resource "aws_iam_role_policy_attachment" "bastion_ssm" {
  role       = aws_iam_role.bastion.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "bastion" {
  name = "${var.project}-bastion"
  role = aws_iam_role.bastion.name
}

# No inbound rules at all: Session Manager connects outbound from the instance's agent,
# so nothing needs to be open TO the bastion. Outbound lets it reach RDS and the SSM service.
resource "aws_security_group" "bastion" {
  name        = "${var.project}-bastion"
  description = "Bastion: no inbound; outbound to RDS + SSM"
  vpc_id      = module.vpc.vpc_id
  tags        = { Name = "${var.project}-bastion" }
}

resource "aws_vpc_security_group_egress_rule" "bastion_all" {
  security_group_id = aws_security_group.bastion.id
  description       = "All outbound (RDS + SSM service)"
  ip_protocol       = "-1"
  cidr_ipv4         = "0.0.0.0/0"
}

# Let the database accept Postgres connections from the bastion (for admin loads).
resource "aws_vpc_security_group_ingress_rule" "db_from_bastion" {
  security_group_id            = aws_security_group.db.id
  description                  = "Postgres from the bastion (admin loads via SSM tunnel)"
  ip_protocol                  = "tcp"
  from_port                    = 5432
  to_port                      = 5432
  referenced_security_group_id = aws_security_group.bastion.id
}

resource "aws_instance" "bastion" {
  ami                         = nonsensitive(data.aws_ssm_parameter.al2023_arm.value)
  instance_type               = "t4g.nano"
  subnet_id                   = module.vpc.public_subnets[0]
  vpc_security_group_ids      = [aws_security_group.bastion.id]
  iam_instance_profile        = aws_iam_instance_profile.bastion.name
  associate_public_ip_address = true # public IP so the SSM agent can reach SSM (we have no NAT)

  tags = { Name = "${var.project}-bastion" }
}

output "bastion_instance_id" {
  value       = aws_instance.bastion.id
  description = "Bastion instance id (the target for the SSM port-forward tunnel)."
}
