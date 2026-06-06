#!/usr/bin/env bash
#
# Is the AWS meter at ~$0? Run this after `terraform destroy` to confirm nothing
# billable is still running. Two checks:
#   1. Terraform's own view (main stack should be empty after destroy; bootstrap keeps
#      the state bucket + DNS zone on purpose).
#   2. Direct probes of the resource types that actually cost money. These are
#      ACCOUNT-WIDE, so if you run other projects in this account, theirs show up too.
#
# Note: this intentionally does NOT use the Resource Groups Tagging API, which lags and
# can show already-deleted resources.

REGION=us-east-1
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== Terraform-managed (this project) =="
printf "  main stack:            %s resource(s)\n" \
  "$(cd "$ROOT/infra/terraform" && terraform state list 2>/dev/null | wc -l | tr -d ' ')"
printf "  bootstrap (persistent): %s resource(s)  (the state bucket + DNS zone, kept by design)\n" \
  "$(cd "$ROOT/infra/terraform/bootstrap" && terraform state list 2>/dev/null | wc -l | tr -d ' ')"

echo
echo "== Billable resources still present? (account-wide) =="
billable=0
report() { # label, value
  if [ -n "$2" ] && [ "$2" != "None" ]; then
    printf "  [PRESENT] %-26s %s\n" "$1" "$2"
    billable=$((billable + 1))
  else
    printf "  [gone]    %s\n" "$1"
  fi
}

report "RDS databases" \
  "$(aws rds describe-db-instances --region "$REGION" --query 'DBInstances[].DBInstanceIdentifier' --output text 2>/dev/null)"
report "Load balancers (ALB/NLB)" \
  "$(aws elbv2 describe-load-balancers --region "$REGION" --query 'LoadBalancers[].LoadBalancerName' --output text 2>/dev/null)"
report "CloudFront distributions" \
  "$(aws cloudfront list-distributions --query 'DistributionList.Items[].Id' --output text 2>/dev/null)"
report "NAT gateways" \
  "$(aws ec2 describe-nat-gateways --region "$REGION" --filter Name=state,Values=available --query 'NatGateways[].NatGatewayId' --output text 2>/dev/null)"
report "EC2 (running/stopped)" \
  "$(aws ec2 describe-instances --region "$REGION" --filters Name=instance-state-name,Values=running,stopped --query 'Reservations[].Instances[].InstanceId' --output text 2>/dev/null)"
report "ECS running tasks (bdr)" \
  "$(aws ecs list-tasks --cluster bdr --region "$REGION" --query 'taskArns' --output text 2>/dev/null)"
report "EBS volumes (unattached)" \
  "$(aws ec2 describe-volumes --region "$REGION" --filters Name=status,Values=available --query 'Volumes[].VolumeId' --output text 2>/dev/null)"
report "Elastic IPs (unassociated)" \
  "$(aws ec2 describe-addresses --region "$REGION" --query 'Addresses[?AssociationId==`null`].PublicIp' --output text 2>/dev/null)"

echo
if [ "$billable" -eq 0 ]; then
  echo "✅ Nothing billable found — the meter is at ~\$0 (state bucket + DNS zone persist by design)."
else
  echo "⚠️  $billable category(ies) above are still present — still billing. (Could be another project in this account.)"
fi
