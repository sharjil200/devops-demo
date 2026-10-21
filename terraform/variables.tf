variable "region" {
  default = "ap-south-1"
}
variable "instance_type" {
  default = "t3.small"
}
variable "public_key_path" {
  default = "~/.ssh/id_rsa.pub"
}
variable "my_ip_cidr" {
  description = "Your public IP, e.g. 1.2.3.4/32"
  type        = string
}
