# GMS:TODO: NGINX front-end? What about load balancing?
resource "google_compute_instance" "kibana" {
    count = "${var.kibana-node-count}"
    name = "kibana-${count.index}"
    machine_type = "${var.kibana_machine_type}"
    zone = "${var.zone}"
    tags = ["elk-kibana"]
    boot_disk {
        auto_delete = "${var.disk_auto_delete}"
        initialize_params {
            image = "debian-cloud/debian-9"
            type = "${var.standard_disk_type}"
            size = 100
        }
    }
    network_interface {
        network = "${var.network}"
        access_config = [{}]
            # GMS:TODO: Need something in here? Currently none of the provisioner stuff is working
#        }
    }
    provisioner "remote-exec" {
#        inline = [
#            "sudo apt-get update",
#            "sudo apt-get -y install default-jdk",
#            "sudo apt-get update",
#            "sudo wget https://artifacts.elastic.co/downloads/kibana/kibana-6.6.0.deb",
#            "sudo wget https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-6.6.0-i386.deb",
#            "sudo dpkg -i kibana-6.6.0.deb",
#            "sudo dpkg -i metricbeat-6.6.0-i386.deb"
#        ]
    }
#    provisioner "file" {
#        content = "configs/kibana.yml"
#        destination = "/etc/kibana"
#    }
#    provisioner "file" {
#        content = "configs/metricbeat.yml"
#        destination = "~"
#    }
#    provisioner "remote-exec" {
#        inline = [
#            "sudo /etc/init.d/kibana start"
#        ]
#    }
}