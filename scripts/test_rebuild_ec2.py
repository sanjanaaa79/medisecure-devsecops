import boto3
import time

ssm = boto3.client('ssm', region_name='us-east-1')
instance_id = 'i-0f92009bba991c492'

cmds = [
    "cd /opt/vle9/app",
    "docker build --no-cache -t medisecure:latest .",
    "echo '=== Trivy Scan of medisecure:latest ==='",
    "trivy image --severity HIGH,CRITICAL medisecure:latest"
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
