# CI/CD: an IAM role that GitHub Actions assumes (via OIDC, no stored AWS keys) to build,
# push, and deploy on every push to main. The OIDC provider already exists in the account
# (kept from a prior project), so we reference it rather than create a duplicate.

data "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"
}

# Trust policy: ONLY GitHub Actions runs in this repo's main branch may assume the role.
data "aws_iam_policy_document" "github_assume" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]
    principals {
      type        = "Federated"
      identifiers = [data.aws_iam_openid_connect_provider.github.arn]
    }
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }
    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:chanys/bounded-deep-research:ref:refs/heads/main"]
    }
  }
}

resource "aws_iam_role" "github_actions" {
  name               = "${var.project}-github-actions"
  assume_role_policy = data.aws_iam_policy_document.github_assume.json
}

# Exactly the permissions the pipeline needs.
data "aws_iam_policy_document" "github_actions" {
  # Authenticate to ECR (this one action can't be resource-scoped).
  statement {
    actions   = ["ecr:GetAuthorizationToken"]
    resources = ["*"]
  }
  # Push images to (and read from) our ECR repo only.
  statement {
    actions = [
      "ecr:BatchCheckLayerAvailability", "ecr:InitiateLayerUpload",
      "ecr:UploadLayerPart", "ecr:CompleteLayerUpload", "ecr:PutImage",
      "ecr:BatchGetImage", "ecr:GetDownloadUrlForLayer",
    ]
    resources = [aws_ecr_repository.app.arn]
  }
  # Register a new task-def revision and roll the service. Register/Describe task-definition
  # don't support resource scoping, hence "*"; the deploy is still bounded to our resources.
  statement {
    actions = [
      "ecs:DescribeTaskDefinition", "ecs:RegisterTaskDefinition",
      "ecs:DescribeServices", "ecs:UpdateService",
    ]
    resources = ["*"]
  }
  # Allow passing ONLY the task execution role when registering a task definition.
  statement {
    actions   = ["iam:PassRole"]
    resources = [aws_iam_role.task_execution.arn]
  }
  # Sync the built frontend to its bucket.
  statement {
    actions   = ["s3:PutObject", "s3:DeleteObject", "s3:ListBucket"]
    resources = [aws_s3_bucket.frontend.arn, "${aws_s3_bucket.frontend.arn}/*"]
  }
  # Invalidate the CloudFront cache (and list distributions so the workflow can find the id).
  statement {
    actions   = ["cloudfront:CreateInvalidation", "cloudfront:ListDistributions"]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "github_actions" {
  name   = "deploy"
  role   = aws_iam_role.github_actions.id
  policy = data.aws_iam_policy_document.github_actions.json
}

output "github_actions_role_arn" {
  value       = aws_iam_role.github_actions.arn
  description = "Role ARN the GitHub Actions workflow assumes (set as needed; the workflow hardcodes it)."
}
