resource "aws_iam_user" "X2033" {
  name        = var.user_name
  path        = "/"
  tags        = var.tags
}

resource "aws_iam_access_key" "X2033" {
  user        = aws_iam_user.X2033.name
}

data "aws_iam_policy_document" "X2033" {
  statement {
    effect    = "Allow"
    actions   = ["*"]
    resources = ["arn:aws:s3:::2033.hex7.com",
                 "arn:aws:s3:::2033.hex7.com/*" ]
  }
}

resource "aws_iam_user_policy" "X2033" {
  name        = var.user_name
  user        = aws_iam_user.X2033.name
  policy      = data.aws_iam_policy_document.X2033.json
}

output "iam_user" {
  value       = aws_iam_access_key.X2033.id
}

output "iam_secret" {
  value       = nonsensitive(aws_iam_access_key.X2033.secret)
  sensitive   = true
}
