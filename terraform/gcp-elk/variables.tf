variable "elastic-node-count" {
    default = "1"
}
variable "kibana-node-count" {
    default = "1"
}
variable "logstash-node-count" {
  default = "1"
}
variable "region" {
  default = "europe-north1"
  type = "string"
}

variable "zone" {
  default = "europe-north1-a"
  type = "string"
}

variable "project" {
  default = "dto-te-prod"
  type = "string"
}

variable "network" {
    default = "elastic-infra"
    type = "string"
}

variable "cluster_name" {
  default = "elk-terraform"
  type = "string"
}

variable "oauth_scopes" {
  default = [
      "compute-rw",
      "storage-ro",
      "logging-write",
      "monitoring",
      # "https://www.googleapis.com/auth/compute",
      # "https://www.googleapis.com/auth/devstorage.read_only",
      # "https://www.googleapis.com/auth/logging.write",
      # "https://www.googleapis.com/auth/monitoring",
  ]
  type = "list"
}

variable "elastic_master_machine_type" {
  default = "n1-standard-2"
  type = "string"
}
variable "elastic_master_disk_type" {
    default = "pd-standard"
    type = "string"
}
variable "elastic_node_machine_type" {
  default = "n1-standard-2"
#  default = "n1-highmem-4"
  type = "string"
}
variable "elastic_node_disk_type" {
  default = "pd-standard"
  type = "string"
}

variable "kibana_machine_type" {
  default = "n1-standard-2"
#  default = "n1-highmem-4"
  type = "string"
}
variable "logstash_machine_type" {
  default = "n1-standard-2"
#  default = "n1-highmem-4"
  type = "string"
}
variable "standard_disk_type" {
  default = "pd-ssd"
  type = "string"
}
variable "disk_auto_delete" {
    description = "Whether or not the disk should be auto-deleted"
    default = true
}
