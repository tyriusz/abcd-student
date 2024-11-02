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
                sh 'trufflehog filesystem ${WORKSPACE} -j > results/trufflehog-secret-scan-report.json || true'
            }
//              post {
//                  always {
//                      defectDojoPublisher(artifact: 'results/trufflehog-secret-scan-report.json',
//                         productName: 'Juice Shop',
//                         scanType: 'Trufflehog Scan',
//                         engagementName: 'piotr.tyrala.mail@gmail.com')
//                  }
//              }
        }
        stage('[OSV-Scanner] Dependency scan') {
            steps {
                sh 'osv-scanner scan --lockfile package-lock.json --format json --output results/sca-osv-scanner.json || true'
            }
//              post {
//                  always {
//                      defectDojoPublisher(artifact: 'results/osv-json-report.json',
//                         productName: 'Juice Shop',
//                         scanType: 'OSV Scan',
//                         engagementName: 'piotr.tyrala.mail@gmail.com')
//                  }
//              }
        }
        stage('[Semgrep] Repository static scan') {
            steps {
                sh 'semgrep --config=auto ${WORKSPACE} --json --output=${WORKSPACE}/results/semgrep-json-report.json || true'
            }
//             post {
//                 always {
//                      defectDojoPublisher(artifact: 'results/semgrep-json-report.json',
//                         productName: 'Juice Shop',
//                         scanType: 'Semgrep JSON Report',
//                         engagementName: 'piotr.tyrala.mail@gmail.com')
//                 }
//             }
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
                         -v /c/Users/Piotrek/Documents/abcd-devsecops/working/abcd-student/.zap:/zap/wrk/:rw \
                         -t ghcr.io/zaproxy/zaproxy:stable bash -c \
                         "zap.sh -cmd -addonupdate; zap.sh -cmd -addoninstall communityScripts -addoninstall pscanrulesAlpha -addoninstall pscanrulesBeta -autorun /zap/wrk/passive_scan.yaml" \
                         || true
                 '''
             }
             post {
                 always {
                     sh '''
                         docker cp zap:/zap/wrk/zap_html_report.html ${WORKSPACE}/results/zap_html_report.html
                         docker cp zap:/zap/wrk/zap_xml_report.xml ${WORKSPACE}/results/zap_xml_report.xml
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
