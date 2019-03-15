A project which was scrapped in favour of a different approach; what there is
works, and has been uploaded in case it proves to be useful.


** WIP **
=========

INFRASTRUCTURE DESIGN?
    - VM: Elasticsearch-0, Metricbeat
    - VM: Elasticsearch-1, Metricbeat
    - VM: Elasticsearch-2, Metricbeat
        - No public IP?
        - SSH only from Bastion # TODO: How did Magnus do this for GHE?
        # TODO: Is 3 nodes enough? Do we want Masters as well?
    - Load Balancer
        - VM: Kibana-0, Metricbeat 
        - VM: Kibana-1, Metricbeat
            - Public traffic both ways
            - SSH only from Bastion
    - Load Balancer
        - VM: Logstash-0, syslog(?), Metricbeat
        - VM: Logstash-1, syslog(?), Metricbeat
            - public traffic inbound only?
            - SSH only from Bastion
    - VM: Bastion
    - Firewall Rules

Terraform's been great for setting up the infrastructure, but lousy at
installing & configuring ELK once the VMs are up - look into Ansible for that?
