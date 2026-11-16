#!/bin/bash
set -e
export HOME=/var/lib/jenkins

echo "=========================================================="
echo " [VLE 9] DevSecOps Pipeline: MediSecure Healthcare System"
echo " Trivy Security Gate + Kubernetes Deployment"
echo "=========================================================="

cd /opt/vle9

echo "=== Stage 1: Build Hardened Docker Image ==="
cd /opt/vle9/app
docker build -t medisecure:latest .
docker images | grep medisecure
cd /opt/vle9

echo "=== Stage 2: Trivy Vulnerability Scanning ==="
echo "Running full vulnerability audit with Trivy..."
trivy image --format table medisecure:latest || true

echo "=== Stage 3: Enforce DevSecOps Security Gate ==="
echo "Gate Rule: Fail build if any HIGH or CRITICAL vulnerabilities exist..."
trivy image --severity HIGH,CRITICAL --exit-code 1 medisecure:latest

echo ">>> SECURITY GATE APPROVED: Zero HIGH and CRITICAL vulnerabilities detected! <<<"

echo "=== Stage 4: Import Image into Kubernetes (K3s) ==="
docker save medisecure:latest | sudo k3s ctr images import -

echo "=== Stage 5: Deploy MediSecure to Kubernetes ==="
sudo kubectl apply -f k8s/deployment.yaml
sudo kubectl apply -f k8s/service.yaml
sudo kubectl apply -f k8s/ingress.yaml
sudo kubectl rollout restart deployment/medisecure-deployment

echo "=== Stage 6: Verify Kubernetes Rollout (2 Replicas) ==="
sudo kubectl rollout status deployment/medisecure-deployment --timeout=90s
echo "Pods Status:"
sudo kubectl get pods -l app=medisecure -o wide
echo "Service Status:"
sudo kubectl get svc medisecure-service -o wide

echo "=== Stage 7: Verify Running Application via NodePort 30090 ==="
sleep 3
echo "Health check endpoint response:"
curl -s -f http://localhost:30090/health
echo ""
echo "Root API endpoint response:"
curl -s http://localhost:30090/
echo ""
echo "Ingress /vle9/ response:"
curl -s http://localhost/vle9/
echo ""

echo "=========================================================="
echo " SUCCESS: MediSecure DevSecOps Pipeline Completed Successfully!"
echo "=========================================================="
