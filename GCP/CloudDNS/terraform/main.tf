terraform {
  backend "gcs" {
      bucket = "terraform_clouddns_prod"
      prefix = "infra/dns"
  }
}

resource "google_project_service" "enable_apis" {
  for_each = toset([
    "dns.googleapis.com",
  ])
  service            = each.key
  disable_on_destroy = false
}


resource "google_dns_managed_zone" "my_new_dns_zone" {
# Creates our Zone in CloudDNS
  name     = var.zone_name
  dns_name = var.zone_dns
  depends_on = [google_project_service.enable_apis,]
}


resource "google_dns_record_set" "my_new_dns_zone" {
# Configures our Zone in CloudDNS
  # Create a wildcard entry for root-level DNS
  name = "*.${google_dns_managed_zone.my_new_dns_zone.dns_name}"
  type = "A"
  ttl  = 300
  managed_zone = google_dns_managed_zone.my_new_dns_zone.name
  rrdatas = [var.zone_allocated_ip_address]
  depends_on = [google_dns_managed_zone.my_new_dns_zone,]
  # NS and SOA records will be auto-created by GCP; the NS records need to be passed to the DNS Team
}


resource "google_dns_record_set" "all_hosts" {
# Creates [A|CNAME] records for single hosts, where the DNS requirements aren't sufficient to justify creating a subdomain
  ttl = 300
  managed_zone = google_dns_managed_zone.my_new_dns_zone.name
  for_each = { for h in var.dns_hosts : h.hostname => h }
  name = "${each.key}.${var.zone_dns}"
  type = each.value.record_type
  rrdatas = [each.value.target_addr]
  depends_on = [google_dns_record_set.my_new_dns_zone,]
}


resource "google_dns_record_set" "all_subdomains" {
# Creates NS records for sub-domains
    type = "NS"
    ttl = 300
    managed_zone = google_dns_managed_zone.my_new_dns_zone.name
    for_each = { for s in var.dns_subdomains : s.subdomain => s }
    name = "${each.key}.${var.zone_dns}"
    rrdatas = each.value.nameservers
    depends_on = [google_dns_record_set.my_new_dns_zone,]
}