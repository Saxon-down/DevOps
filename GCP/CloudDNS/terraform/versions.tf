terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "~> 3.51"
    }
  }
  required_version = ">= 0.13"
}