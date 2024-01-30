resource "aws_iam_user" "x2030" {
  name        = var.user_name
  path        = "/"
  tags        = var.tags
}

resource "aws_iam_access_key" "x2030" {
  user        = aws_iam_user.x2030.name
}

data "aws_iam_policy_document" "x2030" {
  statement {
    effect    = "Allow"
    actions   = ["*"]
    resources = ["arn:aws:s3:::2030.hex7.com",
                 "arn:aws:s3:::2030.hex7.com/*" ]
  }
}

resource "aws_iam_user_policy" "x2030" {
  name        = var.user_name
  user        = aws_iam_user.x2030.name
  policy      = data.aws_iam_policy_document.x2030.json
}

output "iam_user" {
  value       = aws_iam_access_key.x2030.id
}

output "iam_secret" {
  value       = nonsensitive(aws_iam_access_key.x2030.secret)
  sensitive   = true
}
