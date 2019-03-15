# GMS:TODO: NGINX front-end? What about load balancing?
resource "google_compute_instance" "bastion" {
    name = "bastion"
    machine_type = "${var.kibana_machine_type}"
    zone = "${var.zone}"
    tags = ["vm-elk-bastion"]
    boot_disk {
        auto_delete = "${var.disk_auto_delete}"
        initialize_params {
            image = "debian-cloud/debian-9"
            type = "${var.standard_disk_type}"
        }
    }
    network_interface {
        network = "${var.network}"
        access_config = [{}]
            # GMS:TODO: Need something in here? Currently none of the provisioner stuff is working
#        }
    }
    provisioner "file" {
        content = "configs/logstash.yml"
        destination = "/etc/logstash"
    }
}