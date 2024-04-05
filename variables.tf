variable "user_name" {
  type    = string
  default = "X2033"
}

variable "tags" {
  type    = map
  default = {
    product = "X2033"
  }
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "aws_profile" {
  type    = string
  default = "default"
}
