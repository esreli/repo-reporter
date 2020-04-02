#!/usr/bin/env groovy

def agentLabel = 'afdAgent'
def imageName  = 'reporeporter'

pipeline {

    agent {
        label agentLabel
    }

    stages {
        stage('build') {
            steps {
              echo "Going to build docker image ${imageName}"
              script {
                 img = docker.build("${imageName}:${env.BUILD_ID}")
              }

              sh "docker image tag ${imageName}:${env.BUILD_ID} ${imageName}:latest"
            }
        }
    }
}
