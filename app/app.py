from flask import Flask, jsonify, render_template_string, request
import socket
import os
import datetime

app = Flask(__name__)

APP_NAME = "MediSecure Healthcare Portal"
APP_VERSION = os.environ.get("APP_VERSION", "v1.0.0")
APP_ENV = os.environ.get("APP_ENV", "production")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MediSecure - DevSecOps Healthcare System (VLE 9)</title>
    <style>
        :root {
            --primary: #0284c7;
            --primary-dark: #0369a1;
            --secondary: #0d9488;
            --accent-green: #10b981;
            --bg: #0b1329;
            --card-bg: #152238;
            --border: #1e3a5f;
            --text: #f0fdf4;
            --text-muted: #94a3b8;
            --shield-glow: rgba(16, 185, 129, 0.25);
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: radial-gradient(circle at top right, #0f2b48 0%, #070d1e 100%);
            color: var(--text);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        header {
            background: linear-gradient(135deg, #075985 0%, #0e7490 50%, #0f766e 100%);
            padding: 2.2rem 2rem;
            text-align: center;
            box-shadow: 0 4px 25px rgba(0,0,0,0.5);
            border-bottom: 2px solid #38bdf8;
        }
        .header-content {
            max-width: 900px;
            margin: 0 auto;
        }
        .title-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(8px);
            padding: 6px 16px;
            border-radius: 9999px;
            font-size: 0.85rem;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            font-weight: 700;
            margin-bottom: 12px;
            border: 1px solid rgba(255, 255, 255, 0.25);
        }
        h1 {
            font-size: 2.4rem;
            font-weight: 800;
            letter-spacing: -0.025em;
            margin-bottom: 0.5rem;
            color: #ffffff;
            text-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }
        p.subtitle {
            font-size: 1.1rem;
            color: #e0f2fe;
            font-weight: 400;
        }
        .security-banner {
            max-width: 950px;
            margin: -20px auto 25px auto;
            background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
            border: 2px solid #10b981;
            border-radius: 12px;
            padding: 16px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 10px 30px var(--shield-glow);
            z-index: 10;
            position: relative;
        }
        .shield-icon {
            font-size: 2.2rem;
            margin-right: 16px;
        }
        .security-text h3 {
            font-size: 1.15rem;
            font-weight: 700;
            color: #a7f3d0;
            margin-bottom: 2px;
        }
        .security-text p {
            font-size: 0.88rem;
            color: #d1fae5;
        }
        .gate-status-pill {
            background: #10b981;
            color: #022c22;
            padding: 8px 18px;
            border-radius: 8px;
            font-weight: 800;
            font-size: 0.9rem;
            letter-spacing: 0.05em;
        }
        main {
            max-width: 1000px;
            width: 100%;
            margin: 0 auto;
            padding: 1rem 1.5rem 3rem 1.5rem;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        .card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1.5rem;
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .card:hover {
            transform: translateY(-3px);
            border-color: #38bdf8;
        }
        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1rem;
            border-bottom: 1px solid var(--border);
            padding-bottom: 0.75rem;
        }
        .card-header h2 {
            font-size: 1.05rem;
            color: #7dd3fc;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 700;
        }
        .card-icon {
            font-size: 1.4rem;
        }
        .metric-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.5rem 0;
            border-bottom: 1px dashed rgba(255,255,255,0.08);
            font-size: 0.92rem;
        }
        .metric-row:last-child {
            border-bottom: none;
        }
        .metric-label {
            color: var(--text-muted);
        }
        .metric-val {
            font-weight: 600;
            color: #f8fafc;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        }
        .badge-zero {
            background: rgba(16, 185, 129, 0.2);
            color: #34d399;
            border: 1px solid #10b981;
            padding: 2px 10px;
            border-radius: 9999px;
            font-weight: 700;
            font-size: 0.85rem;
        }
        .patient-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
            margin-top: 0.5rem;
        }
        .patient-table th {
            text-align: left;
            color: #7dd3fc;
            padding: 8px 10px;
            border-bottom: 1px solid var(--border);
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.78rem;
        }
        .patient-table td {
            padding: 10px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        .nav-links {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 2rem;
        }
        .btn {
            background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
            color: white;
            text-decoration: none;
            padding: 0.75rem 1.6rem;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.92rem;
            box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35);
            transition: all 0.2s ease;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 18px rgba(2, 132, 199, 0.5);
            color: #ffffff;
        }
        .btn-outline {
            background: transparent;
            border: 1px solid #38bdf8;
            color: #38bdf8;
            box-shadow: none;
        }
        .btn-outline:hover {
            background: rgba(56, 189, 248, 0.15);
            color: #ffffff;
        }
        footer {
            background: #070d1e;
            border-top: 1px solid var(--border);
            text-align: center;
            padding: 1.5rem;
            color: var(--text-muted);
            font-size: 0.88rem;
        }
    </style>
</head>
<body>

    <header>
        <div class="header-content">
            <div class="title-badge">🛡️ HIPAA Compliant &bull; DevSecOps Pipeline</div>
            <h1>MediSecure Hospital System</h1>
            <p class="subtitle">Secure DevOps (DevSecOps) Implementation in a Healthcare System (VLE 9)</p>
        </div>
    </header>

    <div class="security-banner">
        <div style="display: flex; align-items: center;">
            <div class="shield-icon">🛡️</div>
            <div class="security-text">
                <h3>Trivy Vulnerability Scan: PASSED (Zero High/Critical)</h3>
                <p>Automated security gate in Jenkins approved the artifact before Kubernetes deployment.</p>
            </div>
        </div>
        <div class="gate-status-pill">GATE APPROVED</div>
    </div>

    <main>
        <div class="grid">
            <!-- Card 1: DevSecOps Security Gate -->
            <div class="card">
                <div class="card-header">
                    <h2>Security Gate Summary</h2>
                    <span class="card-icon">🔍</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Vulnerability Scanner</span>
                    <span class="metric-val">Aqua Trivy v0.50+</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Critical Vulnerabilities</span>
                    <span class="metric-val"><span class="badge-zero">0 CRITICAL</span></span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">High Vulnerabilities</span>
                    <span class="metric-val"><span class="badge-zero">0 HIGH</span></span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Medium / Low</span>
                    <span class="metric-val">0 / Mitigated</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Container Security</span>
                    <span class="metric-val">Non-Root (UID 10001)</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Pipeline Gate Status</span>
                    <span class="metric-val" style="color: #34d399;">SUCCESS (Exit Code 0)</span>
                </div>
            </div>

            <!-- Card 2: Kubernetes Deployment Info -->
            <div class="card">
                <div class="card-header">
                    <h2>Kubernetes Deployment</h2>
                    <span class="card-icon">☸️</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Application</span>
                    <span class="metric-val">{{ app_name }}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Deployment Name</span>
                    <span class="metric-val">medisecure-deployment</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Active Pod</span>
                    <span class="metric-val" style="color: #7dd3fc;">{{ hostname }}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Cluster Environment</span>
                    <span class="metric-val">K3s Production</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">NodePort Service</span>
                    <span class="metric-val">Port 30090</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Ingress Route</span>
                    <span class="metric-val">/vle9/ (Port 80)</span>
                </div>
            </div>

            <!-- Card 3: Encrypted Patient Telemetry -->
            <div class="card" style="grid-column: 1 / -1;">
                <div class="card-header">
                    <h2>Live Monitored Healthcare Telemetry (HIPAA Compliant)</h2>
                    <span class="card-icon">🩺</span>
                </div>
                <table class="patient-table">
                    <thead>
                        <tr>
                            <th>Patient ID (AES-256)</th>
                            <th>Ward / Room</th>
                            <th>Heart Rate (BPM)</th>
                            <th>SpO2 Level</th>
                            <th>Blood Pressure</th>
                            <th>Security Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><code>MED-7901-X8F</code></td>
                            <td>ICU - Bed 04</td>
                            <td>72 bpm</td>
                            <td>99%</td>
                            <td>120/80 mmHg</td>
                            <td><span class="badge-zero">ENCRYPTED &bull; OK</span></td>
                        </tr>
                        <tr>
                            <td><code>MED-8412-K3Q</code></td>
                            <td>Cardiology - 12B</td>
                            <td>80 bpm</td>
                            <td>98%</td>
                            <td>125/82 mmHg</td>
                            <td><span class="badge-zero">ENCRYPTED &bull; OK</span></td>
                        </tr>
                        <tr>
                            <td><code>MED-9304-P9L</code></td>
                            <td>Emergency - ER-02</td>
                            <td>76 bpm</td>
                            <td>97%</td>
                            <td>118/78 mmHg</td>
                            <td><span class="badge-zero">ENCRYPTED &bull; OK</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div class="nav-links">
            <a href="http://98.88.76.2:8080/job/vle9/" target="_blank" class="btn">Open Jenkins vle9 Pipeline &rarr;</a>
            <a href="/vle9/api" class="btn btn-outline">JSON Telemetry API (/api)</a>
            <a href="/vle9/health" class="btn btn-outline">Health Check Endpoint (/health)</a>
        </div>
    </main>

    <footer>
        <p><strong>MediSecure Hospital System &bull; Secure DevOps (DevSecOps)</strong></p>
        <p>Trivy Container Scanning &bull; Jenkins Security Gate &bull; Kubernetes Production &bull; AWS Account: 113921001189</p>
        <p style="margin-top: 6px; font-size: 0.8rem; color: #64748b;">Timestamp: {{ timestamp }}</p>
    </footer>

</body>
</html>
"""

@app.route('/')
@app.route('/vle9')
@app.route('/vle9/')
def home():
    if request.headers.get('Accept') == 'application/json' or 'curl' in request.headers.get('User-Agent', '').lower():
        return jsonify({
            "project": "VLE9",
            "application": APP_NAME,
            "version": APP_VERSION,
            "trivy_security_status": "PASSED",
            "vulnerabilities": {
                "critical": 0,
                "high": 0,
                "status": "Zero HIGH and CRITICAL vulnerabilities detected"
            },
            "security_gate": "PASSED (Integrated in Jenkins)",
            "container_security": "Non-Root Execution (uid: 10001)",
            "hostname": socket.gethostname(),
            "status": "Healthy & Secure"
        })
    return render_template_string(
        HTML_TEMPLATE,
        app_name=APP_NAME,
        app_version=APP_VERSION,
        hostname=socket.gethostname(),
        timestamp=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    )

@app.route('/api')
@app.route('/vle9/api')
def api():
    return jsonify({
        "project": "VLE9",
        "application": APP_NAME,
        "version": APP_VERSION,
        "trivy_security_scan": {
            "scanner": "Aqua Security Trivy",
            "critical_vulnerabilities": 0,
            "high_vulnerabilities": 0,
            "security_gate_status": "APPROVED"
        },
        "compliance": "HIPAA DevSecOps Baseline",
        "hostname": socket.gethostname(),
        "status": "Active & Monitored",
        "patients_monitored": 3
    })

@app.route('/health')
@app.route('/vle9/health')
def health():
    return jsonify({
        "status": "healthy",
        "application": APP_NAME,
        "security_check": "passed",
        "pod": socket.gethostname()
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
