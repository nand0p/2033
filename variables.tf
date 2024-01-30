variable "user_name" {
  type    = string
  default = "x2030"
}

variable "tags" {
  type    = map
  default = {
    product = "x2030"
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
