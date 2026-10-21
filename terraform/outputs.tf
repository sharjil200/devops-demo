output "public_ip" {
  value = aws_instance.this.public_ip
}
output "app_url" {
  value = "http://${aws_instance.this.public_ip}:5000"
}
output "grafana_url" {
  value = "http://${aws_instance.this.public_ip}:3000"
}
