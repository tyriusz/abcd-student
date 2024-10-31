pipeline {
    agent any
    options {
        skipDefaultCheckout(true)
    }
    stages {
        stage('Code checkout from GitHub main') {
            steps {
                cleanWs()
                checkout scm
            }
        }
        stage('[Prepare directory for test results]') {
            steps {
                sh 'mkdir -p results/'
            }
        }
        stage('[TruffleHog] Secret scan') {
            agent {
                docker {
                    image 'trufflesecurity/trufflehog:latest'
                    args '--entrypoint= -u root' // Wyłączenie ENTRYPOINT i ustawienie użytkownika root
                }
            }
            steps {
                sh '''
                    mkdir -p results/
                    trufflehog filesystem . -j > results/trufflehog-secret-scan-report.json || true
                '''
            }
        }
        stage('[OSV-Scanner] Dependency scan') {
            agent {
                docker {
                    image 'ghcr.io/google/osv-scanner:latest'
                    args '--entrypoint= -u root' // Wyłączenie ENTRYPOINT i ustawienie użytkownika root
                }
            }
            steps {
                sh '''
                    mkdir -p results/
                    osv-scanner --lockfile=package-lock.json \
                                --format=json \
                                --output=results/osv-json-report.json \
                                || true
                '''
            }
        }
        stage('[Semgrep] Repository static scan') {
            agent {
                docker {
                    image 'returntocorp/semgrep'
                    args '--entrypoint= -u root' // Wyłączenie ENTRYPOINT i ustawienie użytkownika root
                }
            }
            steps {
                sh '''
                    mkdir -p results/
                    semgrep --config=auto . \
                            --json \
                            --output=results/semgrep-json-report.json \
                            || true
                '''
            }
        }
        stage('[ZAP] Baseline passive-scan') {
            agent {
                docker {
                    image 'ghcr.io/zaproxy/zaproxy:stable'
                    args '--entrypoint= --network host -u root'
                }
            }
            steps {
                script {
                    // Uruchamiamy Juice Shop na hoście
                    sh '''
                        docker run --name juice-shop -d \
                            -p 3000:3000 \
                            bkimminich/juice-shop
                        sleep 10
                    '''
                    // Tworzymy plik passive_scan.yaml
                    sh '''
                        cat <<EOF > passive_scan.yaml
                        parameters:
                          target: http://localhost:3000
                        EOF
                    '''
                    // Uruchamiamy skanowanie ZAP
                    sh '''
                        zap.sh -cmd -addonupdate
                        zap.sh -cmd -addoninstall communityScripts -addoninstall pscanrulesAlpha -addoninstall pscanrulesBeta
                        zap.sh -daemon -host 0.0.0.0 -port 8090
                        sleep 15
                        zap-cli --zap-url http://localhost:8090 open-url http://localhost:3000
                        zap-cli --zap-url http://localhost:8090 spider http://localhost:3000
                        zap-cli --zap-url http://localhost:8090 active-scan http://localhost:3000
                        mkdir -p results/
                        zap-cli --zap-url http://localhost:8090 report -o results/zap_html_report.html -f html
                        zap-cli --zap-url http://localhost:8090 report -o results/zap_xml_report.xml -f xml
                        zap.sh -cmd -shutdown
                    '''
                }
            }
            post {
                always {
                    sh '''
                        docker stop juice-shop || true
                        docker rm juice-shop || true
                    '''
                }
            }
        }
    }
}