pipeline {
    agent any
    options {
        skipDefaultCheckout(true)
    }
    stages {
        stage('Code checkout from GitHub main') {
            steps {
                script {
                    cleanWs()
                    git credentialsId: 'github-student', url: 'https://github.com/tyriusz/abcd-student', branch: 'main'
                }
            }
        }
        stage('[Prepare directory for test results]') {
            steps {
                sh 'mkdir -p results/'
            }
        }
        stage('[TruffleHog] Secret scan') {
            steps {
                sh '''
                    docker run --name trufflehog \
                        -v abcd-lab:/var/jenkins_home/workspace/devsecops-training:/app:rw \
                        -v /c/Users/Piotrek/Documents/abcd-devsecops/working/results:/results:rw \
                        trufflesecurity/trufflehog:latest \
                        filesystem /app \
                        -j \
                        > results/trufflehog-secret-scan-report.json \
                        || true
                    '''
            }
             post {
                 always {
                     sh '''
                         docker stop trufflehog
                         docker rm trufflehog
                        '''
//                      defectDojoPublisher(artifact: 'results/trufflehog-secret-scan-report.json',
//                         productName: 'Juice Shop',
//                         scanType: 'Trufflehog Scan',
//                         engagementName: 'piotr.tyrala.mail@gmail.com')
                 }
             }
        }
        stage('[OSV-Scanner] Dependency scan') {
            steps {
                sh '''
                    docker run --name osv-scanner \
                        -v abcd-lab:/var/jenkins_home/workspace/devsecops-training:/app:rw \
                        -v /c/Users/Piotrek/Documents/abcd-devsecops/working/results:/results:rw \
                        ghcr.io/google/osv-scanner:latest \
                        --lockfile=/app/package-lock.json \
                        --format=json \
                        --output=abcd-lab:/var/jenkins_home/workspace/devsecops-training/results/osv-json-report.json \
                        || true
                    '''
            }
             post {
                 always {
                     sh '''
                         docker stop osv-scanner
                         docker rm osv-scanner
                     '''
//                      defectDojoPublisher(artifact: 'results/osv-json-report.json',
//                         productName: 'Juice Shop',
//                         scanType: 'OSV Scan',
//                         engagementName: 'piotr.tyrala.mail@gmail.com')
                 }
             }
        }
        stage('[Semgrep] Repository static scan') {
            steps {
                sh '''
                    docker run --name semgrep \
                        -v abcd-lab:/var/jenkins_home/workspace/devsecops-training:/app:rw \
                        returntocorp/semgrep semgrep \
                        --config=auto /app \
                        --json \
                        --output=abcd-lab:/var/jenkins_home/workspace/devsecops-training/results/semgrep-json-report.json \
                        || true
                '''
            }
            post {
                always {
                    sh '''
                        docker stop semgrep
                        docker rm semgrep
                    '''
//                      defectDojoPublisher(artifact: 'results/semgrep-json-report.json',
//                         productName: 'Juice Shop',
//                         scanType: 'Semgrep JSON Report',
//                         engagementName: 'piotr.tyrala.mail@gmail.com')
                }
            }
        }
         stage('[ZAP] Baseline passive-scan') {
             steps {
                 sh '''
                     docker run --name juice-shop -d \
                         -p 3000:3000 \
                         bkimminich/juice-shop
                     sleep 5
                 '''
                 sh '''
                     docker run --name zap \
                         --add-host=host.docker.internal:host-gateway \
                         -v abcd-lab:/var/jenkins_home/workspace/devsecops-training/.zap:/zap/wrk/:rw \
                         -t ghcr.io/zaproxy/zaproxy:stable bash -c \
                         "zap.sh -cmd -addonupdate; zap.sh -cmd -addoninstall communityScripts -addoninstall pscanrulesAlpha -addoninstall pscanrulesBeta -autorun /zap/wrk/passive_scan.yaml" \
                         || true
                 '''
             }
             post {
                 always {
                     sh '''
                         docker stop zap juice-shop
                         docker rm zap juice-shop
                     '''
//                      defectDojoPublisher(artifact: 'results/zap_xml_report.xml',
//                         productName: 'Juice Shop',
//                         scanType: 'ZAP Scan',
//                         engagementName: 'piotr.tyrala.mail@gmail.com')
                 }
             }
         }
    }
}
