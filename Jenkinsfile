#!/usr/bin/env groovy

pipeline {

    agent { label "master" }

    environment {
        AZURE_SUBSCRIPTION_ID = credentials('az_subscription_id')
        AZURE_CLIENT_ID = credentials('az_client_id')
        AZURE_SECRET = credentials('az_secret')
        AZURE_TENANT = credentials('az_tenant')
		SCRIPT_PATH = "${WORKSPACE}/scripts"
        SOURCE_IP = sh(returnStdout: true, script: "${SCRIPT_PATH}/get-source-ip.py")
    }

    stages {

        // clean out the existing workspace
        stage ('clean workspace') {
            steps {
                cleanWs deleteDirs: true    
            }
        }

        // perform a checkout of the repo specified in the Jenkins job
        stage('checkout') {
            steps {
                 checkout scm  
            }
        }

        stage('cloud build') {

			steps {
				wrap([$class: 'AnsiColorBuildWrapper', colorMapName: "xterm"]) {
					sh 'ansible-playbook site.yml \
										--extra-vars "source_ip=${SOURCE_IP}"
				}
			}
    }
}