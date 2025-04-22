pipeline {
    agent any
    stages {
      
        stage('run application') {
            steps {
                script {
                    sh """
                        echo 'running configuration script'
                        python3 /etc/ansible/main.py
                    """
                }
            }
        }
        
        stage('unit testing') {
            steps {
                script {
                    sh """
                        echo 'running unit tests'
                    """
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished with status: ${currentBuild.currentResult}"
            emailext (
                subject: "Job '${env.JOB_NAME}' (${env.BUILD_NUMBER}) Completed",
                body: "Job '${env.JOB_NAME}' is complete. The status is: $currentBuild.currentResult}\nURL provided for more detail: ${env.BUILD_URL}",
                to: "james.vaughan@colorado.edu",
            )
        }
        success {
            echo 'Pipeline completed successfully'
        }
        failure {
            echo 'Pipeline failure'
        }
    }
}
