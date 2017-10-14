resource "aws_instance" "bastion" {
		ami = "${var.ami_id}"
    instance_type = "t2.micro"
    key_name = "${var.ssh_key_name}"
    subnet_id = "${element(split(",", var.subnet_list), 5)}"
    vpc_security_group_ids = ["${aws_security_group.bastion.id}"]
    associate_public_ip_address = true

    tags {
      Name = "bastion-${var.name}"
      Role = "bastion"
    }
}

resource "aws_security_group" "bastion" {
  name = "restricted"
  description = "restricted by user IP"
   ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["${var.user_ip}/32"]
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
    prefix_list_ids = ["pl-12c4e678"]
  }
}

resource "aws_route53_record" "bastion" {
  zone_id = "${data.aws_route53_zone.dns_zone.zone_id}"
  name = "${var.name}.${data.aws_route53_zone.dns_zone.name}"
  type = "A"
  records = ["${aws_instance.bastion.public_ip}"]
}