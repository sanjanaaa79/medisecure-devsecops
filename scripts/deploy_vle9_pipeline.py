import boto3
import time
import os

ssm = boto3.client('ssm', region_name='us-east-1')
instance_id = 'i-0f92009bba991c492'

base_dir = r'c:\Users\Sanjana Mukherjee\Desktop\Projects\pbl3\vle9'

with open(os.path.join(base_dir, 'app', 'app.py'), 'r', encoding='utf-8') as f:
    app_py = f.read()
with open(os.path.join(base_dir, 'app', 'requirements.txt'), 'r', encoding='utf-8') as f:
    req_txt = f.read()
with open(os.path.join(base_dir, 'app', 'Dockerfile'), 'r', encoding='utf-8') as f:
    dock_file = f.read()
with open(os.path.join(base_dir, 'k8s', 'deployment.yaml'), 'r', encoding='utf-8') as f:
    k8s_deploy = f.read()
with open(os.path.join(base_dir, 'k8s', 'service.yaml'), 'r', encoding='utf-8') as f:
    k8s_svc = f.read()
with open(os.path.join(base_dir, 'k8s', 'ingress.yaml'), 'r', encoding='utf-8') as f:
    k8s_ing = f.read()
with open(os.path.join(base_dir, 'run_pipeline.sh'), 'r', encoding='utf-8') as f:
    pipe_sh = f.read()

setup_cmds = [
    "mkdir -p /opt/vle9/app /opt/vle9/k8s",
    f"cat << 'EOF' > /opt/vle9/app/app.py\n{app_py}\nEOF",
    f"cat << 'EOF' > /opt/vle9/app/requirements.txt\n{req_txt}\nEOF",
    f"cat << 'EOF' > /opt/vle9/app/Dockerfile\n{dock_file}\nEOF",
    f"cat << 'EOF' > /opt/vle9/k8s/deployment.yaml\n{k8s_deploy}\nEOF",
    f"cat << 'EOF' > /opt/vle9/k8s/service.yaml\n{k8s_svc}\nEOF",
    f"cat << 'EOF' > /opt/vle9/k8s/ingress.yaml\n{k8s_ing}\nEOF",
    f"cat << 'EOF' > /opt/vle9/run_pipeline.sh\n{pipe_sh}\nEOF",
    "chmod +x /opt/vle9/run_pipeline.sh",
    "chown -R jenkins:jenkins /opt/vle9"
]

print("1. Syncing updated Dockerfile and manifests to /opt/vle9...")
r1 = ssm.send_command(InstanceIds=[instance_id], DocumentName='AWS-RunShellScript', Parameters={'commands': setup_cmds}, TimeoutSeconds=120)
cmd_id1 = r1['Command']['CommandId']
while True:
    time.sleep(5)
    inv1 = ssm.get_command_invocation(CommandId=cmd_id1, InstanceId=instance_id)
    if inv1['Status'] in ['Success', 'Failed', 'TimedOut', 'Cancelled']:
        print("Sync Status:", inv1['Status'])
        break

print("\n2. Triggering Jenkins build #2 for vle9 (DevSecOps with Trivy Gate)...")
build_cmds = [
    "curl -u admin:admin123 -X POST http://localhost:8080/job/vle9/build",
    "sleep 6",
    "for i in {1..50}; do BUILDING=$(curl -s -u admin:admin123 http://localhost:8080/job/vle9/lastBuild/api/json | grep -o '\"building\":true' || echo ''); if [ -z \"$BUILDING\" ]; then echo 'Build completed!'; break; fi; echo \"DevSecOps Pipeline running... ($i/50)\"; sleep 4; done",
    "echo '=== DevSecOps Pipeline Console Log ==='",
    "curl -s -u admin:admin123 http://localhost:8080/job/vle9/lastBuild/consoleText | tail -n 45",
    "echo ''",
    "echo '=== Testing Live NodePort 30090 ==='",
    "curl -s http://localhost:30090/",
    "echo ''",
    "echo '=== Testing Ingress /vle9/ ==='",
    "curl -s http://localhost/vle9/",
    "echo ''",
    "echo '=== Kubernetes Pods Status ==='",
    "sudo kubectl get pods -l app=medisecure -o wide",
    "sudo kubectl get svc medisecure-service"
]

r2 = ssm.send_command(InstanceIds=[instance_id], DocumentName='AWS-RunShellScript', Parameters={'commands': build_cmds}, TimeoutSeconds=400)
cmd_id2 = r2['Command']['CommandId']
while True:
    time.sleep(10)
    inv2 = ssm.get_command_invocation(CommandId=cmd_id2, InstanceId=instance_id)
    print("Build Status check:", inv2['Status'])
    if inv2['Status'] in ['Success', 'Failed', 'TimedOut', 'Cancelled']:
        print("Build Finished with Status:", inv2['Status'])
        print(inv2.get('StandardOutputContent',''))
        print(inv2.get('StandardErrorContent',''))
        break
