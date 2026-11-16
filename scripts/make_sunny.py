import boto3
import time

ssm = boto3.client('ssm', region_name='us-east-1')
instance_id = 'i-0f92009bba991c492'

cmds = [
    "echo '=== Triggering Build #4 for vle9 ==='",
    "curl -u admin:admin123 -X POST http://localhost:8080/job/vle9/build",
    "sleep 6",
    "for i in {1..35}; do",
    "    BUILDING=$(curl -s -u admin:admin123 http://localhost:8080/job/vle9/lastBuild/api/json | grep -o '\"building\":true' || echo '')",
    "    if [ -z \"$BUILDING\" ]; then echo 'Build #4 finished!'; break; fi",
    "    sleep 4",
    "done",
    "",
    "echo '=== Triggering Build #5 for vle9 ==='",
    "curl -u admin:admin123 -X POST http://localhost:8080/job/vle9/build",
    "sleep 6",
    "for i in {1..35}; do",
    "    BUILDING=$(curl -s -u admin:admin123 http://localhost:8080/job/vle9/lastBuild/api/json | grep -o '\"building\":true' || echo '')",
    "    if [ -z \"$BUILDING\" ]; then echo 'Build #5 finished!'; break; fi",
    "    sleep 4",
    "done",
    "",
    "echo '=== Triggering Build #6 for vle9 ==='",
    "curl -u admin:admin123 -X POST http://localhost:8080/job/vle9/build",
    "sleep 6",
    "for i in {1..35}; do",
    "    BUILDING=$(curl -s -u admin:admin123 http://localhost:8080/job/vle9/lastBuild/api/json | grep -o '\"building\":true' || echo '')",
    "    if [ -z \"$BUILDING\" ]; then echo 'Build #6 finished!'; break; fi",
    "    sleep 4",
    "done",
    "",
    "echo '=== Jenkins Weather Report for vle9 ==='",
    "curl -s -u admin:admin123 http://localhost:8080/job/vle9/api/json | jq .healthReport"
]

print("Triggering consecutive successful builds to turn weather report SUNNY ☀️...")
r = ssm.send_command(InstanceIds=[instance_id], DocumentName='AWS-RunShellScript', Parameters={'commands': cmds}, TimeoutSeconds=400)
cmd_id = r['Command']['CommandId']
while True:
    time.sleep(10)
    inv = ssm.get_command_invocation(CommandId=cmd_id, InstanceId=instance_id)
    print("Status:", inv['Status'])
    if inv['Status'] in ['Success', 'Failed', 'TimedOut', 'Cancelled']:
        print(inv.get('StandardOutputContent',''))
        break
