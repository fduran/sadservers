# Debian

packer {
  required_plugins {
    amazon = {
      version = "= 1.2.1"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

source "amazon-ebs" "debian" {
  ami_name                    = "scenario-1-saintjohn"
  instance_type               = "t3a.nano"
  region                      = "${var.region}"
  vpc_id                      = "${var.vpc_id}"
  subnet_id                   = "${var.subnet_id}"
  associate_public_ip_address = true
  source_ami                  = "${var.source_ami}"
  ssh_username                = "admin"
}

build {
  name = "debian-build"
  sources = [
    "source.amazon-ebs.debian"
  ]

  # OS & scenario packages
  provisioner "shell" {
    inline = [
      "echo Update packages...",
      "sudo apt-get update",
      "sudo apt-get install -y lsof",
    ]
  }

  # badlog.py
  provisioner "file" {
    source      = "../files/badlog.py"
    destination = "/tmp/badlog.py"
  }

  provisioner "shell" {
    inline = [
      "mv /tmp/badlog.py /home/admin/badlog.py",
      "chmod +x /home/admin/badlog.py",
      "sudo touch /var/log/bad.log",
      "sudo chown admin: /var/log/bad.log",
      "echo '@reboot /home/admin/badlog.py &' | crontab -",
    ]
  }

  # check.sh
  provisioner "file" {
    source      = "../files/check.sh"
    destination = "/tmp/check.sh"
  }

  provisioner "shell" {
    inline = [
      "sudo mv /tmp/check.sh /home/admin/agent/check.sh",
      "sudo chmod +x /home/admin/agent/check.sh",
    ]
  }

}
