#resource "google_compute_disk" "elastic-nodes-disk" {
#    count = "${var.elastic-node-count}"
#    name = "elasticsearch-data-${count.index}"
#    type = "${var.elastic_node_disk_type}"
#    zone = "${var.zone}"
#    size = "1000"
#}

resource "google_compute_instance" "elastic-nodes" {
    count = "${var.elastic-node-count}"
    name = "elasticsearch-node-${count.index}"
    machine_type = "${var.elastic_node_machine_type}"
    zone = "${var.zone}"
    tags = ["elasticsearch", "elk-ssh"]
    boot_disk {
        auto_delete = "${var.disk_auto_delete}"
        initialize_params {
            image = "debian-cloud/debian-9"
            type = "${var.elastic_node_disk_type}"
            size = 1000
        }
    }
    network_interface {
        network = "${var.network}"
        access_config = [{}]
    }
    # GMS:TODO: none of the provisioner stuff is being run - think something's timing out. Maybe put it all in a script, upload it and then execute the script?
    provisioner "remote-exec" {
        # GMS:TODO: Move all of this to ansible? Or upload and run script?
#        inline = [
#            "sudo apt-get update",
#            "sudo apt-get -y install default-jdk",
#            "sudo apt-get update",
#            "sudo wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.6.1.deb",
#            "sudo wget https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-6.6.1-amd64.deb",
#            "sudo dpkg -i elasticsearch-6.6.0.deb",
#            "sudo /usr/share/elasticsearch/bin/elasticsearch-plugin install -b discovery-gce",
#            "sudo dpkg -i metricbeat-6.6.0-amd64.deb"
#        ]
        # use sudo wget to pull config files down from github?
        # .. wget is installed already
        # GMS:WORKING: These are confirmed file locations
        # /etc/elasticsearch/elasticsearch.yml
        # /etc/metricbeat/metricbeat.yml
        # python 3.5.3 installed (call as python3, since 2.7.13 installed too)
    }
#    provisioner "file" {
#        content = "configs/elasticsearch.yml"
#        destination = "/etc/elasticsearch"
#    }
#    provisioner "file" {
#        content = "configs/metricbeat.yml"
#        destination = "~"
#    }
#    provisioner "remote-exec" {
#        inline = [
#            "sudo /etc/init.d/elasticsearch start"
#        ]
#    }
}