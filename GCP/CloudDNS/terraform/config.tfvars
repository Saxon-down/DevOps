# GCP
project = "my-gcp-project"
region = "europe-west1"

# DNS
# These settings are used for configuring CloudDNS and should not be changed
name_prefix = "dev"
zone_name = "xxx-yyy-com"
zone_dns = "xxx.yyy.com."
zone_allocated_ip_address = "127.0.0.1"

# SUBDOMAINS
dns_subdomains = [
    {
        subdomain = "subdomain1"
        nameservers = [
            "ns-cloud-e1.googledomains.com.",
            "ns-cloud-e2.googledomains.com.",
            "ns-cloud-e3.googledomains.com.",
            "ns-cloud-e4.googledomains.com."
        ]
    },
    {
        subdomain = "subdomain2"
        nameservers = [
            "ns-cloud-d1.googledomains.com.",
            "ns-cloud-d2.googledomains.com.",
            "ns-cloud-d3.googledomains.com.",
            "ns-cloud-d4.googledomains.com."
       ]
    }
]

# Individual DNS Records
# Note: we support A records only; if your setup is more complicated, you should set up a subdomain and use that. See the main README.md
dns_hosts = [
    {
        hostname = "arecord1"
        target_addr = "127.0.0.1"
        record_type = "A" 
    },
    {
        hostname = "arecord2"
        target_addr = "127.0.0.2"
        record_type = "A" 

    },
    {
        hostname = "cnamerecord1"
        target_addr = "arecord1.xxx.yyy.com."
        record_type = "CNAME" 
    },
    {
        hostname = "cnamerecord2"
        target_addr = "arecord2.xxx.yyy.com."
        record_type = "CNAME" 
    }
]
