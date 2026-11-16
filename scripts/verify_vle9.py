import boto3
import time

ssm = boto3.client('ssm', region_name='us-east-1')
instance_id = 'i-0f92009bba991c492'

cmds = [
    "echo '=== 1. JENKINS BUILD #3 STATUS ==='",
    "curl -s -u admin:admin123 http://localhost:8080/job/vle9/3/api/json | jq {number,result,duration,timestamp}",
    "echo ''",
    "echo '=== 2. KUBERNETES PODS & 2 REPLICAS ==='",
    "sudo kubectl get pods -l app=medisecure -o wide",
    "echo ''",
    "echo '=== 3. KUBERNETES SERVICE & NODEPORT 30090 ==='",
    "sudo kubectl get svc medisecure-service -o wide",
    "sudo kubectl describe svc medisecure-service | grep -E 'Endpoints|NodePort'",
    "echo ''",
    "echo '=== 4. DIRECT NODEPORT 30090 RESPONSE ==='",
    "curl -s http://localhost:30090/",
    "echo ''",
    "echo '=== 5. INGRESS PORT 80 (/vle9/) RESPONSE ==='",
    "curl -s http://localhost/vle9/",
    "echo ''",
    "echo '=== 6. HEALTH ENDPOINT ==='",
    "curl -s http://localhost/vle9/health",
    "echo ''",
    "echo '=== 7. TELEMETRY API ENDPOINT ==='",
    "curl -s http://localhost/vle9/api",
    "echo ''"
]

r = ssm.send_command(InstanceIds=[instance_id], DocumentName='AWS-RunShellScript', Parameters={'commands': cmds}, TimeoutSeconds=120)
cmd_id = r['Command']['CommandId']
while True:
    time.sleep(5)
    inv = ssm.get_command_invocation(CommandId=cmd_id, InstanceId=instance_id)
    if inv['Status'] in ['Success', 'Failed', 'TimedOut', 'Cancelled']:
        print(inv.get('StandardOutputContent',''))
        break
