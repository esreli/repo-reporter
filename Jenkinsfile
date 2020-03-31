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
              echo "Going to build docker image ${iamgeName}"
              script {
                 docker.build("${imageName}:${env.BUILD_ID}")
              }
            }
        }
    }
}
