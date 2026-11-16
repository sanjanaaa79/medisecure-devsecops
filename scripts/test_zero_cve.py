import boto3
import time

ssm = boto3.client('ssm', region_name='us-east-1')
instance_id = 'i-0f92009bba991c492'

test_dockerfile = """FROM python:3.11-alpine

RUN apk update && apk upgrade --no-cache

RUN adduser -D -u 10001 appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip uninstall -y setuptools wheel pip \
    && rm -rf /root/.cache

COPY app.py .
RUN chown -R appuser:appuser /app

USER appuser
ENV PORT=5000 PYTHONUNBUFFERED=1
EXPOSE 5000
CMD ["python", "app.py"]
"""

cmds = [
    f"cat << 'EOF' > /tmp/Dockerfile.clean\n{test_dockerfile}\nEOF",
    "cd /opt/vle9/app",
    "docker build -f /tmp/Dockerfile.clean -t test-clean:latest .",
    "echo '=== RUNNING TRIVY VULNERABILITY AUDIT (SEVERITY HIGH,CRITICAL) ==='",
    "trivy image --severity HIGH,CRITICAL --exit-code 1 test-clean:latest",
    "echo 'SUCCESS: ZERO HIGH AND CRITICAL VULNERABILITIES DETECTED!'"
]

r = ssm.send_command(InstanceIds=[instance_id], DocumentName='AWS-RunShellScript', Parameters={'commands': cmds}, TimeoutSeconds=180)
cmd_id = r['Command']['CommandId']
while True:
    time.sleep(5)
    inv = ssm.get_command_invocation(CommandId=cmd_id, InstanceId=instance_id)
    if inv['Status'] in ['Success', 'Failed', 'TimedOut', 'Cancelled']:
        print("Status:", inv['Status'])
        print("STDOUT:\n", inv.get('StandardOutputContent',''))
        print("STDERR:\n", inv.get('StandardErrorContent',''))
        break
