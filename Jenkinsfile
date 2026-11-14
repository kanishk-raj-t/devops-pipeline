pipeline {
    agent any

    triggers {
        pollSCM('* * * * *')
    }

    stages {
        stage('Setup Environment') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh '. venv/bin/activate && pytest -v'
            }
        }

        stage('Build & Package') {
            steps {
                sh 'tar -czf todo-api-build.tar.gz app.py requirements.txt'
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: 'todo-api-build.tar.gz', fingerprint: true
        }
    }
}