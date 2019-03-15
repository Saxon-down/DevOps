resource "google_compute_network" "default" {
    name = "${var.network}"
    description = "ELK infrastructure network"
    auto_create_subnetworks = "true"
}
resource "google_compute_subnetwork" "default" {
    name = "${var.network}"
    ip_cidr_range = "10.128.0.0/20"
    network = "${google_compute_network.default.self_link}"
    region = "${var.region}"
    private_ip_google_access = true
}
resource "google_compute_firewall" "ssh" {
    name = "elk-ssh-access"
    network = "${var.network}"
    allow {
        protocol = "tcp"
        ports = ["22"]
    }
#    source_tags = ["elk-bastion"]
    target_tags = ["vm-elk-bastion"]
}
# GMS:TODO: What other firewall rules do we need?
resource "google_compute_firewall" "github" {
    name = "elk-github"
    network = "${var.network}"
    allow {
        protocol = "tcp"
        ports = ["5010"]
    }
    target_tags = ["vm-elk-logstash"]
}
resource "google_compute_firewall" "jira" {
    # GMS:TODO: PLACEHOLDER - don't know the actual values yet
    name = "elk-jira"
    network = "${var.network}"
    allow {
        protocol = "tcp"
        ports = ["5011"]
    }
    target_tags = ["vm-elk-logstash"]
}
resource "google_compute_firewall" "artifactory" {
    # GMS:TODO: PLACEHOLDER - don't know the actual values yet
    name = "elk-artifactory"
    network = "${var.network}"
    allow {
        protocol = "tcp"
        ports = ["5012"]
    }
    target_tags = ["vm-elk-logstash"]
}
# GMS:TODO: disable default rules for SSH and RDC (or at least, restrict them to BASTION host)
# GMS:TODO: 
