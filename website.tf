resource "aws_s3_bucket_public_access_block" "X2033_website" {
  bucket                  = var.s3_bucket
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}


resource "aws_s3_bucket_acl" "X2033_website" {
  depends_on = [
    aws_s3_bucket_public_access_block.X2033_website
  ]
  bucket = var.s3_bucket
  acl    = "public-read"
}


resource "aws_s3_bucket_website_configuration" "X2033_website" {
  bucket = var.s3_bucket
  index_document { suffix = "index.html" }
}


resource "aws_s3_bucket_policy" "X2033_website" {
  bucket = var.s3_bucket
  policy = data.aws_iam_policy_document.X2033_website.json
}


data "aws_iam_policy_document" "X2033_website" {
  statement {
    sid    = "AllowPublicRead"
    effect = "Allow"
    resources = [
      "arn:aws:s3:::${var.s3_bucket}",
      "arn:aws:s3:::${var.s3_bucket}/*",
    ]
    actions = ["S3:Get*", "S3:List*"]
    principals {
      type        = "*"
      identifiers = ["*"]
    }
  }
}

resource "aws_s3_bucket_ownership_controls" "X2033_website" {
  bucket = var.s3_bucket
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}
