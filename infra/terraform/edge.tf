# Edge layer: TLS certificates, the HTTPS entry points, the static frontend (S3 +
# CloudFront), and the DNS records that point your subdomain at them.
#
#   browser --HTTPS--> CloudFront --> S3 (static frontend)     = answertrail.yeesengchan.com
#   browser --HTTPS--> ALB --------> Fargate (the API, SSE)    = api.answertrail.yeesengchan.com
#
# Both ACM certificates live in us-east-1 (our region), which is also the region
# CloudFront requires its certificate in, so no second-region juggling is needed.

data "aws_caller_identity" "current" {}

# The hosted zone created in ./bootstrap. We look it up by name rather than hardcoding
# its id, so the two configs stay decoupled.
data "aws_route53_zone" "project" {
  name = var.domain
}

# ===========================================================================
# TLS certificates (one for the API on the ALB, one for the frontend on CloudFront)
# ===========================================================================
resource "aws_acm_certificate" "api" {
  domain_name       = "api.${var.domain}"
  validation_method = "DNS"
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_acm_certificate" "frontend" {
  domain_name       = var.domain
  validation_method = "DNS"
  lifecycle {
    create_before_destroy = true
  }
}

# ACM proves domain ownership by checking for a DNS record it specifies. We create those
# records in the hosted zone; because the zone is delegated to Route 53, ACM can see them
# and the certificate validates automatically.
resource "aws_route53_record" "api_cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.api.domain_validation_options : dvo.domain_name => {
      name = dvo.resource_record_name, type = dvo.resource_record_type, record = dvo.resource_record_value
    }
  }
  zone_id         = data.aws_route53_zone.project.zone_id
  name            = each.value.name
  type            = each.value.type
  records         = [each.value.record]
  ttl             = 60
  allow_overwrite = true
}

resource "aws_route53_record" "frontend_cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.frontend.domain_validation_options : dvo.domain_name => {
      name = dvo.resource_record_name, type = dvo.resource_record_type, record = dvo.resource_record_value
    }
  }
  zone_id         = data.aws_route53_zone.project.zone_id
  name            = each.value.name
  type            = each.value.type
  records         = [each.value.record]
  ttl             = 60
  allow_overwrite = true
}

# These resources make Terraform WAIT until each certificate is validated before anything
# downstream (the listener, CloudFront) tries to use it.
resource "aws_acm_certificate_validation" "api" {
  certificate_arn         = aws_acm_certificate.api.arn
  validation_record_fqdns = [for r in aws_route53_record.api_cert_validation : r.fqdn]
}

resource "aws_acm_certificate_validation" "frontend" {
  certificate_arn         = aws_acm_certificate.frontend.arn
  validation_record_fqdns = [for r in aws_route53_record.frontend_cert_validation : r.fqdn]
}

# ===========================================================================
# HTTPS on the ALB (the API). The plain HTTP :80 listener in compute.tf stays as a
# fallback; browsers use this HTTPS one via api.<domain>.
# ===========================================================================
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = aws_acm_certificate_validation.api.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

# ===========================================================================
# Frontend hosting: a private S3 bucket served through CloudFront
# ===========================================================================
resource "aws_s3_bucket" "frontend" {
  bucket = "${var.project}-frontend-${data.aws_caller_identity.current.account_id}"
}

# The bucket is private; only CloudFront reads it (via the access control below).
resource "aws_s3_bucket_public_access_block" "frontend" {
  bucket                  = aws_s3_bucket.frontend.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Origin Access Control = the modern way to let ONLY this CloudFront distribution read
# the private bucket (no public bucket, no legacy origin-access-identity).
resource "aws_cloudfront_origin_access_control" "frontend" {
  name                              = "${var.project}-frontend"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

# Static export emits files like query.html, but routes are requested as /query. This
# tiny function rewrites the URL so the right file is served: "/" -> index.html, a path
# with no file extension -> append .html, anything with an extension is left alone.
resource "aws_cloudfront_function" "rewrite" {
  name    = "${var.project}-rewrite"
  runtime = "cloudfront-js-2.0"
  code    = <<-JS
    function handler(event) {
      var request = event.request;
      var uri = request.uri;
      if (uri.endsWith('/')) {
        request.uri += 'index.html';
      } else if (!uri.includes('.')) {
        request.uri += '.html';
      }
      return request;
    }
  JS
}

# Managed AWS cache policy tuned for static sites (caches by URL, compresses).
data "aws_cloudfront_cache_policy" "optimized" {
  name = "Managed-CachingOptimized"
}

resource "aws_cloudfront_distribution" "frontend" {
  enabled             = true
  default_root_object = "index.html"
  aliases             = [var.domain]
  price_class         = "PriceClass_100" # cheapest: North America + Europe edges only

  origin {
    domain_name              = aws_s3_bucket.frontend.bucket_regional_domain_name
    origin_id                = "frontend-s3"
    origin_access_control_id = aws_cloudfront_origin_access_control.frontend.id
  }

  default_cache_behavior {
    target_origin_id       = "frontend-s3"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    cache_policy_id        = data.aws_cloudfront_cache_policy.optimized.id

    function_association {
      event_type   = "viewer-request"
      function_arn = aws_cloudfront_function.rewrite.arn
    }
  }

  # Serve the static 404 page for missing files.
  custom_error_response {
    error_code         = 403
    response_code      = 404
    response_page_path = "/404.html"
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate_validation.frontend.certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
}

# Let CloudFront (and only this distribution) read objects from the private bucket.
data "aws_iam_policy_document" "frontend_bucket" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.frontend.arn}/*"]
    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "AWS:SourceArn"
      values   = [aws_cloudfront_distribution.frontend.arn]
    }
  }
}

resource "aws_s3_bucket_policy" "frontend" {
  bucket = aws_s3_bucket.frontend.id
  policy = data.aws_iam_policy_document.frontend_bucket.json
}

# ===========================================================================
# DNS: point the domain names at CloudFront and the ALB (ALIAS records)
# ===========================================================================
resource "aws_route53_record" "frontend" {
  zone_id = data.aws_route53_zone.project.zone_id
  name    = var.domain
  type    = "A"
  alias {
    name                   = aws_cloudfront_distribution.frontend.domain_name
    zone_id                = aws_cloudfront_distribution.frontend.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "api" {
  zone_id = data.aws_route53_zone.project.zone_id
  name    = "api.${var.domain}"
  type    = "A"
  alias {
    name                   = aws_lb.main.dns_name
    zone_id                = aws_lb.main.zone_id
    evaluate_target_health = false
  }
}

output "frontend_url" {
  value       = "https://${var.domain}"
  description = "The live site."
}

output "api_url" {
  value       = "https://api.${var.domain}"
  description = "The API base (what the frontend calls)."
}

output "frontend_bucket" {
  value       = aws_s3_bucket.frontend.id
  description = "S3 bucket to sync the built frontend (out/) into."
}

output "cloudfront_distribution_id" {
  value       = aws_cloudfront_distribution.frontend.id
  description = "CloudFront distribution id (for cache invalidations)."
}
