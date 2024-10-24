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
        stage('[BEFORE TESTS]') {
            steps {
                echo 'Hello!!'
                sh 'whoami'
                sh 'mkdir -p results/'
            }
        }
//         stage('[OSV-Scanner] Dependency scan') {
//             steps {
//                 sh '''
//                     docker run --name osv-scanner \
//                         -v /c/Users/Piotrek/Documents/abcd-devsecops/working/abcd-student:/app:rw \
//                         ghcr.io/google/osv-scanner:latest \
//                         --lockfile=/app/package-lock.json \
//                         --format=json \
//                         --output=/app/osv/osv-json-report.json \
//                         || true
//                     '''
//             }
//              post {
//                  always {
//                      sh '''
//                          docker cp osv-scanner:/app/osv/osv-json-report.json ${WORKSPACE}/results/osv-json-report.json
//                          docker stop osv-scanner
//                          docker rm osv-scanner
//                      '''
//                      defectDojoPublisher(artifact: 'results/osv-json-report.json',
//                         productName: 'Juice Shop',
//                         scanType: 'OSV Scan',
//                         engagementName: 'piotr.tyrala.mail@gmail.com')
//                  }
//              }
//         }

        stage('[TruffleHog] Secret scan') {
            steps {
                sh '''
                    docker pull trufflesecurity/trufflehog:latest || true
                    docker run --name trufflehog \
                        -v /c/Users/Piotrek/Documents/abcd-devsecops/working/abcd-student:/app:rw \
                        trufflesecurity/trufflehog:latest \
                        'trufflehog filesystem /app --json /app/trufflehog-report.json' \
                        || true
                    '''
            }
//              post {
//                  always {
//                      sh '''
//                          docker cp trufflehog:/app/reports/trufflehog-report.json ${WORKSPACE}/results/trufflehog-report.json
//                          docker stop trufflehog
//                          docker rm trufflehog
//                      '''
//                      defectDojoPublisher(artifact: 'results/trufflehog-report.json',
//                         productName: 'Juice Shop',
//                         scanType: 'Trufflehog Scan',
//                         engagementName: 'piotr.tyrala.mail@gmail.com')
//                  }
//              }
        }



//         stage('[ZAP] Baseline passive-scan') {
//             steps {
//                 sh '''
//                     docker run --name juice-shop -d \
//                         -p 3000:3000 \
//                         bkimminich/juice-shop
//                     sleep 5
//                 '''
//                 sh '''
//                     docker run --name zap \
//                         --add-host=host.docker.internal:host-gateway \
//                         -v /c/Users/Piotrek/Documents/abcd-devsecops/working/abcd-student/.zap:/zap/wrk/:rw \
//                         -t ghcr.io/zaproxy/zaproxy:stable bash -c \
//                         "zap.sh -cmd -addonupdate; zap.sh -cmd -addoninstall communityScripts -addoninstall pscanrulesAlpha -addoninstall pscanrulesBeta -autorun /zap/wrk/passive_scan.yaml" \
//                         || true
//                 '''
//             }
//             post {
//                 always {
//                     sh '''
//                         docker cp zap:/zap/wrk/zap_html_report.html ${WORKSPACE}/results/zap_html_report.html
//                         docker cp zap:/zap/wrk/zap_xml_report.xml ${WORKSPACE}/results/zap_xml_report.xml
//                         docker stop zap juice-shop
//                         docker rm zap juice-shop
//                     '''
//                     defectDojoPublisher(artifact: 'results/zap_xml_report.xml',
//                        productName: 'Juice Shop',
//                        scanType: 'ZAP Scan',
//                        engagementName: 'piotr.tyrala.mail@gmail.com')
//                 }
//             }
//         }
    }
}
