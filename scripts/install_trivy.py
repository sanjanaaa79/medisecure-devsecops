import boto3
import time

ssm = boto3.client('ssm', region_name='us-east-1')
instance_id = 'i-0f92009bba991c492'

cmds = [
    "if ! command -v trivy &> /dev/null; then",
    "    echo 'Installing Trivy standalone binary...'",
    "    curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sudo sh -s -- -b /usr/local/bin",
    "fi",
    "trivy --version"
]

print("Checking and installing Trivy on EC2...")
r = ssm.send_command(InstanceIds=[instance_id], DocumentName='AWS-RunShellScript', Parameters={'commands': cmds}, TimeoutSeconds=180)
cmd_id = r['Command']['CommandId']
while True:
    time.sleep(5)
    inv = ssm.get_command_invocation(CommandId=cmd_id, InstanceId=instance_id)
    if inv['Status'] in ['Success', 'Failed', 'TimedOut', 'Cancelled']:
        print('Status:', inv['Status'])
        print('STDOUT:\n', inv.get('StandardOutputContent',''))
        print('STDERR:\n', inv.get('StandardErrorContent',''))
        break
