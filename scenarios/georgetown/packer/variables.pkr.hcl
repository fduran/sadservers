# variables for Packer file, adapt to your AWS region, base image, vpc, subnet

variable "region" {
  type    = string
  default = "us-east-1"
}

# tested with source Debian 11 image HVM 64-bit (x86)
# change to one in your region
variable "source_ami" {
  type    = string
  default = "ami-"
}

# change to your vpc
variable "vpc_id" {
  type    = string
  default = "vpc-"
}

# change to your subnet
variable "subnet_id" {
  type    = string
  default = "subnet-"
}