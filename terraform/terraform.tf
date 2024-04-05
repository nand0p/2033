provider "aws" {
  profile = var.aws_profile
  region  = var.aws_region
}

terraform {
  backend "s3" {
    bucket  = "2033-tf"
    key     = "X2033.tfstate"
    region  = "us-east-1"
    encrypt = true
    profile = "default"
  }
}
