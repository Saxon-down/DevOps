# CloudDNS

Terraform setup for a new CloudDNS server, using the xxx.yyy.com domain. This was written only to support sub-domains, and A & CNAME records.

## Running Terraform to update DNS

### The following environment variables need to be set before running:

export GOOGLE_APPLICATION_CREDENTIALS=<path_to_credentials.json_file>


### If this is the first time the Terraform scripts have been run (for the current project)

You'll need to manually create a bucket, to store the terraform state. In GCP, go to STORAGE -> Storage and click CREATE BUCKET. Set it up with the following details:

* NAME: has to be unique, and recorded in main.tf in the 'terraform {
  backend "gcs" {' block at the top.
* multi-region
* Storage Class: Standard
* Acceess Control: fine-grained


### Running Terraform

`
cd terraform
terraform init --backend-config=./config.backend --reconfigure
terraform apply --var-file=./config.tfvars
`