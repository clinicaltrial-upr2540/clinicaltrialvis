terraform {
  backend "s3" {
    bucket = "clinicaltrial-terraform"
    key    = "terraform/terraform_dev.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region                  = "us-east-1"
  shared_credentials_file = "~/.aws/creds"
  profile                 = "default"
}
