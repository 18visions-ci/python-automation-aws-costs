pipeline {
  agent any

  environment {
    DISCORD_WEBHOOK_URL = credentials('discord_webhook') // Jenkins credential ID
    AWS_ACCESS_KEY_ID = credentials('aws_access_key')
    AWS_SECRET_ACCESS_KEY = credentials('aws_secret_key')
    AWS_DEFAULT_REGION = 'us-east-1'
  }

  stages {
    stage('Build Docker Image') {
      steps {
        script {
          dockerImage = docker.build('aws-cost-reporter')
        }
      }
    }

    stage('Run Cost Reporter') {
      steps {
        script {
          dockerImage.run(
            "-e DISCORD_WEBHOOK_URL=${DISCORD_WEBHOOK_URL} " +
            "-e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} " +
            "-e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} " +
            "-e AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}"
          )
        }
      }
    }
  }

  post {
    always {
      script {
        try {
          sh 'docker rmi aws-cost-reporter || true'
        } catch (Exception e) {
          echo "Image cleanup failed: ${e.getMessage()}"
        }
      }
    }
  }
}
