variable "project" {
  description = "The GCP project name."
  type        = string
}

variable "region" {
  description = "The region in which the infrastructure will be deployed."
  type        = string
}

variable "name_prefix" {
  description = "A name prefix used in resource names (will be prepended) to ensure uniqueness across a project."
  type        = string
}

variable "zone_name" {
    description = "Name of the zone in CloudDNS, e.g. xxx-yyy-com"
    type = string
}

variable "zone_dns" {
    description = "Root DNS name, e.g. xxx.yyy.com"
    type = string
}

variable "zone_allocated_ip_address" {
    description = "IP address for 'zone_dns', which has been allocated by the DNS Team"
    type = string
}

variable "dns_subdomains" {
    description = "Used for creating NAMESERVER entries in CloudDNS; these will point to CloudDNS Zones which have been created in other GCP Projects"
    type = list(object({
        subdomain = string
        nameservers = list(string)
    }))
    default = [
        {
            subdomain = ""
            nameservers = []
        }
    ]    
}

variable "dns_hosts" {
    description = "Used for creating A/CNAME RECORD entries in CloudDNS; these should only be used for very simple setups"
    type = list(object({
        hostname = string
        ip_addr = string
        record_type = string
    }))
    default = [
        {
            hostname = ""
            target_addr = ""
            record_type = ""
        }
    ]
}