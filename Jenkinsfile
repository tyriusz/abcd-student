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
        }
        stage('[OSV-Scanner] Dependency scan') {
            steps {
                sh 'osv-scanner scan --lockfile package-lock.json --format sarif --output results/sca-osv-report.sarif || true'
            }
        }
        stage('[Semgrep] Repository static scan') {
            steps {
                sh 'semgrep --config=auto ${WORKSPACE} --sarif --output=results/semgrep-report.sarif || true'
            }
//             post {
//                 always {
//                     recordIssues tools: [sarif(pattern: '**/results/semgrep-report.sarif')]
//                 }
//             }
        }
//          stage('[ZAP] Baseline passive-scan') {
//              steps {
//                  sh '''
//                      docker run --name juice-shop -d \
//                          -p 3000:3000 \
//                          bkimminich/juice-shop
//                      sleep 5
//                  '''
//                  sh '''
//                      docker run --name zap \
//                          --add-host=host.docker.internal:host-gateway \
//                          -v /c/Users/Piotrek/Documents/abcd-devsecops/working/abcd-student/.zap:/zap/wrk/:rw \
//                          -t ghcr.io/zaproxy/zaproxy:stable bash -c \
//                          "zap.sh -cmd -addonupdate; zap.sh -cmd -addoninstall communityScripts -addoninstall pscanrulesAlpha -addoninstall pscanrulesBeta -autorun /zap/wrk/passive_scan.yaml" \
//                          || true
//                  '''
//              }
//              post {
//                  always {
//                      sh '''
//                          docker cp zap:/zap/wrk/zap_html_report.html ${WORKSPACE}/results/zap_html_report.html
//                          docker cp zap:/zap/wrk/zap_xml_report.xml ${WORKSPACE}/results/zap_xml_report.xml
//                      '''
//                  }
//              }
//          }
    }
             post {
                 always {
                     recordIssues(
                         tools: [
                             sarif(id: 'Trufflehog', name: 'Trufflehog', pattern: '**/results/trufflehog-secret-scan-report.json'),
                             sarif(id: 'Semgrep', name: 'Semgrep', pattern: '**/results/semgrep-report.sarif'),
                             sarif(id: 'OSV-Scanner', name: 'OSV-Scanner', pattern: '**/results/sca-osv-report.sarif'),
//                              owaspZap(id: 'ZAP', name: 'OWASP ZAP', pattern: '**/results/zap_xml_report.xml')
//                              sarif(id: 'ZAP', name: 'OWASP ZAP', pattern: '**/results/zap_sarif_report.json')
                         ]
                     )
                  }
             }
}
