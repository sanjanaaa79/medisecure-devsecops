# VLE 9: Secure DevOps (DevSecOps) Implementation in a Healthcare System

This project demonstrates a production-grade **DevSecOps pipeline** for a healthcare application (**MediSecure**) using **Jenkins**, **Aqua Security Trivy**, **Docker**, and **Kubernetes (K3s)** on AWS EC2.

---

## 🎯 Objectives Fulfilled

1. **MediSecure Docker application created:**
   - Containerized HIPAA-compliant healthcare portal with live patient telemetry and vital monitoring.
   - Built on a hardened base image (`python:3.11-slim`) running as non-root user (`appuser:10001`).
2. **Trivy vulnerability scanning integrated:**
   - Aqua Security Trivy integrated into the Jenkins CI/CD pipeline.
   - Comprehensive container image vulnerability analysis performed before deployment.
3. **Zero HIGH and CRITICAL vulnerabilities detected:**
   - Scan results confirm **0 HIGH** and **0 CRITICAL** vulnerabilities detected.
4. **Security gate integrated into Jenkins:**
   - Automated quality gate enforces `trivy image --severity HIGH,CRITICAL --exit-code 1 medisecure:latest`.
   - Pipeline automatically blocks and aborts if any high/critical CVEs exist.
5. **Successfully deployed to Kubernetes:**
   - Deployed to Kubernetes cluster (`medisecure-deployment`) with 2 replicas and secure pod security context (`runAsNonRoot: true`).
6. **Verified running application:**
   - Verified via Kubernetes NodePort `30090`, Ingress Port 80 at `/vle9/`, and local Docker Desktop container on port `5053`.

---

## 🛡️ DevSecOps Pipeline Architecture

```
[ Developer Commit ]
         │
         ▼
[ Jenkins Pipeline: vle9 ]
         │
         ├─── Stage 1: Build Docker Image (medisecure:latest)
         │
         ├─── Stage 2: Trivy Vulnerability Scan
         │             (Scans OS packages & Python dependencies)
         │
         ├─── Stage 3: DevSecOps Security Gate
         │             RULE: trivy --severity HIGH,CRITICAL --exit-code 1
         │             [PASSED: 0 High, 0 Critical]
         │
         ├─── Stage 4: Import to K3s Container Runtime
         │
         ├─── Stage 5: Deploy to Kubernetes Cluster (2 Replicas)
         │
         └─── Stage 6: Rollout & NodePort 30090 Health Verification
                       [LIVE PRODUCTION HEALTHCARE SYSTEM]
```

---

## 🌐 Endpoints & Verification Links

| Component | URL | Description |
| :--- | :--- | :--- |
| **MediSecure Web Application (Ingress)** | [http://98.88.76.2/vle9/](http://98.88.76.2/vle9/) | Live production portal on port 80 |
| **MediSecure Direct NodePort** | [http://98.88.76.2:30090/](http://98.88.76.2:30090/) | Direct Kubernetes NodePort endpoint |
| **Jenkins DevSecOps Job (`vle9`)** | [http://98.88.76.2:8080/job/vle9/](http://98.88.76.2:8080/job/vle9/) | Jenkins DevSecOps pipeline with Trivy gate |
| **Local Docker Desktop Container** | [http://localhost:5053/](http://localhost:5053/) | Local test container `medisecure-local` |

---

## 📁 Repository Structure

```
.
├── .gitignore
├── Jenkinsfile                    # Declarative DevSecOps pipeline with Trivy gate
├── README.md                      # Documentation & security architecture
├── run_pipeline.sh                # End-to-end pipeline execution script
├── app/
│   ├── Dockerfile                 # Hardened, non-root Dockerfile (python:3.11-slim)
│   ├── app.py                     # MediSecure healthcare portal & telemetry API
│   └── requirements.txt           # Pinned, secure dependencies
├── k8s/
│   ├── deployment.yaml            # Kubernetes deployment (2 replicas, non-root)
│   ├── service.yaml               # NodePort service on port 30090
│   └── ingress.yaml               # Traefik Ingress routing /vle9 on port 80
└── scripts/                       # Deployment and verification automation scripts
```

---

## 👤 Author
- **Developer:** Sanjana Mukherjee
- **AWS Account:** `113921001189`
- **GitHub:** [https://github.com/sanjanaaa79/medisecure-devsecops](https://github.com/sanjanaaa79/medisecure-devsecops)
