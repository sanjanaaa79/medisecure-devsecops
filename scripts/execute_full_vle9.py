import boto3
import time
import os

ssm = boto3.client('ssm', region_name='us-east-1')
instance_id = 'i-0f92009bba991c492'

base_dir = r'c:\Users\Sanjana Mukherjee\Desktop\Projects\pbl3\vle9'

with open(os.path.join(base_dir, 'app', 'Dockerfile'), 'r', encoding='utf-8') as f:
    dock_file = f.read()
with open(os.path.join(base_dir, 'run_pipeline.sh'), 'r', encoding='utf-8') as f:
    pipe_sh = f.read()

setup_cmds = [
    f"cat << 'EOF' > /opt/vle9/app/Dockerfile\n{dock_file}\nEOF",
    f"cat << 'EOF' > /opt/vle9/run_pipeline.sh\n{pipe_sh}\nEOF",
    "chmod +x /opt/vle9/run_pipeline.sh",
    "chown -R jenkins:jenkins /opt/vle9",
    "echo 'Updated Dockerfile and run_pipeline.sh in /opt/vle9!'"
]

print("1. Updating /opt/vle9 on EC2...")
r1 = ssm.send_command(InstanceIds=[instance_id], DocumentName='AWS-RunShellScript', Parameters={'commands': setup_cmds}, TimeoutSeconds=120)
cmd_id1 = r1['Command']['CommandId']
while True:
    time.sleep(5)
    inv1 = ssm.get_command_invocation(CommandId=cmd_id1, InstanceId=instance_id)
    if inv1['Status'] in ['Success', 'Failed', 'TimedOut', 'Cancelled']:
        print("Update Status:", inv1['Status'])
        break

print("\n2. Triggering Jenkins build #3 for vle9 (DevSecOps with Trivy Gate)...")
build_cmds = [
    "curl -u admin:admin123 -X POST http://localhost:8080/job/vle9/build",
    "sleep 6",
    "for i in {1..50}; do BUILDING=$(curl -s -u admin:admin123 http://localhost:8080/job/vle9/lastBuild/api/json | grep -o '\"building\":true' || echo ''); if [ -z \"$BUILDING\" ]; then echo 'Build completed!'; break; fi; echo \"DevSecOps Pipeline running... ($i/50)\"; sleep 5; done",
    "echo '=== DevSecOps Pipeline Console Log (Last 45 lines) ==='",
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
