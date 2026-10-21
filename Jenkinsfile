pipeline {
  agent any

  environment {
    IMAGE_NAME = "sharjil200/devops-demo"
    EC2_HOST   = "ubuntu@65.2.73.161"
    TAG        = "${env.BUILD_NUMBER}"
  }

  stages {
    stage('Test') {
      steps {
        sh '''
          docker run --rm -u $(id -u):$(id -g) -e HOME=/tmp -e PYTHONDONTWRITEBYTECODE=1 \
            -v "$PWD/app":/app -w /app python:3.12-slim \
            sh -c "pip install -q --user -r requirements.txt && python -m pytest -q -p no:cacheprovider"
        '''
      }
    }

    stage('Build') {
      steps {
        sh 'docker build --build-arg APP_VERSION=$TAG -t $IMAGE_NAME:$TAG -t $IMAGE_NAME:latest .'
      }
    }

    stage('Push') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                          usernameVariable: 'U', passwordVariable: 'P')]) {
          sh '''
            echo "$P" | docker login -u "$U" --password-stdin
            docker push $IMAGE_NAME:$TAG
            docker push $IMAGE_NAME:latest
          '''
        }
      }
    }

    stage('Deploy') {
      steps {
        sshagent(['ec2-ssh']) {
          sh '''
            ssh -o StrictHostKeyChecking=no $EC2_HOST "mkdir -p ~/devops-demo"
            scp -o StrictHostKeyChecking=no -r docker-compose.yml monitoring $EC2_HOST:~/devops-demo/
            ssh -o StrictHostKeyChecking=no $EC2_HOST \
              "cd ~/devops-demo && export IMAGE=$IMAGE_NAME:$TAG && docker compose pull app && docker compose up -d"
          '''
        }
      }
    }

    stage('Smoke Test') {
      steps {
        sh '''
          HOST=$(echo $EC2_HOST | cut -d@ -f2)
          for i in 1 2 3 4 5 6; do
            curl -fs http://$HOST:5000/health && exit 0
            sleep 5
          done
          echo "Smoke test failed"; exit 1
        '''
      }
    }
  }

  post {
    always  { sh 'docker image prune -f || true' }
    failure { echo 'Pipeline failed. Check the stage logs.' }
  }
}
