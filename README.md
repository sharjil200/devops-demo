# DevOps Demo: end-to-end, solo

Flask app -> Jenkins CI/CD -> Docker Hub -> EC2 (Terraform) -> Prometheus + Grafana

## 1. Run locally
    docker compose up -d --build
    curl localhost:5000/health
    # Prometheus: :9090  Grafana: :3000 (admin/admin)

## 2. Provision infra
    cd terraform
    terraform init
    terraform apply -var="my_ip_cidr=$(curl -s ifconfig.me)/32"
    # note the public_ip output

## 3. Jenkins setup
- Credentials: `dockerhub-creds` (username/password), `ec2-ssh` (SSH private key, user ubuntu)
- Plugins: Pipeline, SSH Agent, Credentials Binding
- Jenkins agent needs Docker installed
- Edit IMAGE_NAME and EC2_HOST in Jenkinsfile
- Create a Pipeline job from this repo (SCM), add a GitHub webhook

## 4. Grafana
Add Prometheus data source `http://prometheus:9090`, then import dashboard ID 3662 or graph:
- `rate(http_requests_total[1m])`
- `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))`

## 5. Destroy
    cd terraform && terraform destroy
