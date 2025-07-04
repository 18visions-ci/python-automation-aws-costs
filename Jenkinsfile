pipeline {
  agent any

  triggers {
    cron('TZ=America/Los_Angeles\nH 10 * * *')
  }

  environment {
    DISCORD_WEBHOOK_URL = credentials('discord_webhook')
    AWS_ACCESS_KEY_ID = credentials('aws_access_key')
    AWS_SECRET_ACCESS_KEY = credentials('aws_secret_key')
    AWS_DEFAULT_REGION = 'us-west-2'
    DOCKER_IMAGE = 'registry-prod.iworksometimes.com/python-automation-aws-costs:latest'
  }

  stages {
    stage('Pull Docker Image') {
      steps {
        sh 'docker pull $DOCKER_IMAGE'
      }
    }

    stage('Run Cost Reporter') {
      steps {
        sh '''
          docker run --rm \
            -e DISCORD_WEBHOOK_URL=$DISCORD_WEBHOOK_URL \
            -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
            -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
            -e AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION \
            $DOCKER_IMAGE
        '''
      }
    }
  }

  post {
    always {
      script {
        try {
          sh 'docker rmi $DOCKER_IMAGE || true'
        } catch (Exception e) {
          echo "Image cleanup failed: ${e.getMessage()}"
        }
      }
    }
  }
}
