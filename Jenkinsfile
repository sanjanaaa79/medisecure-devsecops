pipeline {
    agent any

    environment {
        APP_NAME = 'medisecure'
        IMAGE_NAME = 'medisecure:latest'
        K8S_DEPLOYMENT = 'medisecure-deployment'
        NODEPORT = '30090'
    }

    stages {
        stage('Checkout & Setup') {
            steps {
                echo "=== Stage 1: Checkout & Workspace Setup ==="
                sh 'cd /opt/vle9 && ls -la'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "=== Stage 2: Build Hardened Docker Image ==="
                sh '''
                    cd /opt/vle9/app
                    docker build -t ${IMAGE_NAME} .
                    docker images | grep medisecure
                '''
            }
        }

        stage('Trivy Security Gate') {
            steps {
                echo "=== Stage 3: Trivy Vulnerability Scanning & Security Gate ==="
                sh '''
                    echo "Scanning Docker image ${IMAGE_NAME} with Trivy..."
                    trivy image --format table ${IMAGE_NAME}
                    
                    echo "Enforcing Security Gate: Blocking build on any HIGH or CRITICAL vulnerabilities..."
                    trivy image --severity HIGH,CRITICAL --exit-code 1 ${IMAGE_NAME}
                    
                    echo "SECURITY GATE PASSED: Zero HIGH and CRITICAL vulnerabilities detected!"
                '''
            }
        }

        stage('Import to K3s Runtime') {
            steps {
                echo "=== Stage 4: Import Image into Kubernetes Container Runtime ==="
                sh '''
                    docker save ${IMAGE_NAME} | sudo k3s ctr images import -
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "=== Stage 5: Deploy MediSecure to Kubernetes ==="
                sh '''
                    cd /opt/vle9
                    sudo kubectl apply -f k8s/deployment.yaml
                    sudo kubectl apply -f k8s/service.yaml
                    sudo kubectl apply -f k8s/ingress.yaml
                    sudo kubectl rollout restart deployment/${K8S_DEPLOYMENT}
                '''
            }
        }

        stage('Verify Rollout & Replicas') {
            steps {
                echo "=== Stage 6: Verify Kubernetes Rollout & Replicas ==="
                sh '''
                    sudo kubectl rollout status deployment/${K8S_DEPLOYMENT} --timeout=90s
                    sudo kubectl get pods -l app=medisecure -o wide
                    sudo kubectl get svc medisecure-service
                '''
            }
        }

        stage('Verify Running Application') {
            steps {
                echo "=== Stage 7: Verify Running Application & Endpoints ==="
                sh '''
                    sleep 3
                    echo "Verifying NodePort ${NODEPORT}..."
                    curl -s -f http://localhost:${NODEPORT}/health || exit 1
                    echo ""
                    curl -s http://localhost:${NODEPORT}/
                    echo ""
                    echo "SUCCESS: MediSecure DevSecOps Pipeline Completed Successfully!"
                '''
            }
        }
    }

    post {
        success {
            echo "SUCCESS: MediSecure application passed Trivy security gate and is running on Kubernetes!"
        }
        failure {
            echo "FAILED: Pipeline failed. Check Trivy vulnerability report or deployment logs."
        }
    }
}
