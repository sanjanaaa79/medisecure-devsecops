import boto3
import time

ssm = boto3.client('ssm', region_name='us-east-1')
instance_id = 'i-0f92009bba991c492'

cmds = [
    """python3 -c "
import subprocess, json
raw = subprocess.check_output(['trivy', 'image', '--severity', 'HIGH,CRITICAL', '--format', 'json', 'test-alpine:latest'])
data = json.loads(raw)
for r in data.get('Results', []):
    vulns = r.get('Vulnerabilities')
    if vulns:
        print(r['Target'], '-->', [(v['PkgName'], v['VulnerabilityID'], v['InstalledVersion'], v.get('FixedVersion')) for v in vulns])
" """
]

r = ssm.send_command(InstanceIds=[instance_id], DocumentName='AWS-RunShellScript', Parameters={'commands': cmds}, TimeoutSeconds=60)
cmd_id = r['Command']['CommandId']
time.sleep(6)
inv = ssm.get_command_invocation(CommandId=cmd_id, InstanceId=instance_id)
print("OUT:\n", inv.get('StandardOutputContent',''))
print("ERR:\n", inv.get('StandardErrorContent',''))
