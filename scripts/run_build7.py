import boto3
import time

ssm = boto3.client('ssm', region_name='us-east-1')
instance_id = 'i-0f92009bba991c492'

cmds = [
    "curl -u admin:admin123 -X POST http://localhost:8080/job/vle9/build",
    "sleep 6",
    "for i in {1..35}; do",
    "    BUILDING=$(curl -s -u admin:admin123 http://localhost:8080/job/vle9/lastBuild/api/json | grep -o '\"building\":true' || echo '')",
    "    if [ -z \"$BUILDING\" ]; then echo 'Build finished!'; break; fi",
    "    sleep 3",
    "done",
    "curl -s -u admin:admin123 http://localhost:8080/job/vle9/api/json | jq .healthReport"
]

r = ssm.send_command(InstanceIds=[instance_id], DocumentName='AWS-RunShellScript', Parameters={'commands': cmds}, TimeoutSeconds=120)
cmd_id = r['Command']['CommandId']
while True:
    time.sleep(6)
    inv = ssm.get_command_invocation(CommandId=cmd_id, InstanceId=instance_id)
    if inv['Status'] in ['Success', 'Failed', 'TimedOut', 'Cancelled']:
        print(inv.get('StandardOutputContent',''))
        break
