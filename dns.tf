data "aws_route53_zone" "hex7" {
  name = "hex7.com."
}


resource "aws_route53_record" "X2033" {
  zone_id = data.aws_route53_zone.hex7.zone_id
  name    = "${var.s3_bucket}."
  type    = "A"
  alias {
    name                   = aws_cloudfront_distribution.X2033.domain_name
    zone_id                = aws_cloudfront_distribution.X2033.hosted_zone_id
    evaluate_target_health = true
  }
}
