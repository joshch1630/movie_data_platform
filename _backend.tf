terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.44.0"
    }
  }
  backend "s3" {
    bucket = "movie-data-platform.mdp.backend-state"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
  required_version = "> 0.14"
}