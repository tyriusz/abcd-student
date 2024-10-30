pipeline {
    agent any
    options {
        skipDefaultCheckout(true)
    }
    environment {
        WORKSPACE_DIR = "${env.WORKSPACE}"
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
                    docker run --rm \
                        -v "${WORKSPACE_DIR}":/app \
                        trufflesecurity/trufflehog:latest \
                        filesystem /app \
                        -j \
                        > trufflehog-secret-scan-report.json \
                        || true
                '''
            }
            post {
                always {
                    sh 'cat results/trufflehog-secret-scan-report.json'
//                     defectDojoPublisher(artifact: 'results/trufflehog-secret-scan-report.json',
//                         productName: 'Juice Shop',
//                         scanType: 'Trufflehog Scan',
//                         engagementName: 'piotr.tyrala.mail@gmail.com')
                }
            }
        }
        stage('[OSV-Scanner] Dependency scan') {
            steps {
                sh '''
                    docker run --rm \
                        -v "${WORKSPACE_DIR}":/app \
                        ghcr.io/google/osv-scanner:latest \
                        --lockfile=/app/package-lock.json \
                        --format=json \
                        --output=osv-json-report.json \
                        || true
                '''
            }
            post {
                always {
                    sh 'cat osv-json-report.json'
//                     defectDojoPublisher(artifact: 'results/osv-json-report.json',
//                         productName: 'Juice Shop',
//                         scanType: 'OSV Scan',
//                         engagementName: 'piotr.tyrala.mail@gmail.com')
                }
            }
        }
        stage('[Semgrep] Repository static scan') {
            steps {
                sh '''
                    docker run --rm \
                        -v "${WORKSPACE_DIR}":/app \
                        returntocorp/semgrep semgrep \
                        --config=auto /app \
                        --json \
                        --output=semgrep-json-report.json \
                        || true
                '''
            }
            post {
                always {
                    sh 'cat semgrep-json-report.json'
//                     defectDojoPublisher(artifact: 'results/semgrep-json-report.json',
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
                    docker run --name zap --rm \
                        --add-host=host.docker.internal:host-gateway \
                        -v "${WORKSPACE_DIR}/.zap":/zap/wrk/:rw \
                        ghcr.io/zaproxy/zaproxy:stable bash -c \
                        "zap.sh -cmd -addonupdate; \
                         zap.sh -cmd -addoninstall communityScripts -addoninstall pscanrulesAlpha -addoninstall pscanrulesBeta -autorun /zap/wrk/passive_scan.yaml" \
                        || true
                '''
            }
            post {
                always {
                    sh '''
                        docker cp zap:/zap/wrk/zap_html_report.html ${WORKSPACE_DIR}/results/zap_html_report.html || true
                        docker cp zap:/zap/wrk/zap_xml_report.xml ${WORKSPACE_DIR}/results/zap_xml_report.xml || true
                        docker stop zap juice-shop || true
                        docker rm zap juice-shop || true
                    '''
//                     defectDojoPublisher(artifact: 'results/zap_xml_report.xml',
//                         productName: 'Juice Shop',
//                         scanType: 'ZAP Scan',
//                         engagementName: 'piotr.tyrala.mail@gmail.com')
                }
            }
        }
    }
}