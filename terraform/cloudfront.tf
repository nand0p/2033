data "aws_s3_bucket" "X2033" {
  bucket = var.s3_bucket
}

resource "aws_cloudfront_distribution" "X2033" {
  origin {
    domain_name              = data.aws_s3_bucket.X2033.bucket_regional_domain_name
    origin_access_control_id = aws_cloudfront_origin_access_control.X2033.id
    origin_id                = "X2033"
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "X2033"
  default_root_object = "index.html"

  logging_config {
    include_cookies = false
    bucket          = "2033-logs.s3.amazonaws.com"
    prefix          = "cloudfront"
  }

  aliases = ["2033.hex7.com"]

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "X2033"

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "allow-all"
    min_ttl                = 0
    default_ttl            = 60
    max_ttl                = 300
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  tags = var.tags

  viewer_certificate {
    acm_certificate_arn = aws_acm_certificate.X2033.id
    ssl_support_method  = "sni-only"
  }

}


resource "aws_s3_bucket" "X2033-logs" {
  bucket = "2033-logs"
}

resource "aws_s3_bucket_acl" "X2033-logs" {
  bucket = aws_s3_bucket.X2033-logs.id
  acl    = "log-delivery-write"
}

resource "aws_s3_bucket_public_access_block" "X2033-logs" {
  bucket                  = aws_s3_bucket.X2033-logs.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_ownership_controls" "X2033-logs" {
  bucket                  = aws_s3_bucket.X2033-logs.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}


resource "aws_acm_certificate" "X2033" {
  domain_name       = var.s3_bucket
  validation_method = "EMAIL"

  tags = {
    Environment = "2033.hex7.com"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_cloudfront_origin_access_control" "X2033" {
  name                              = "X2033"
  description                       = "X2033 Policy"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}
