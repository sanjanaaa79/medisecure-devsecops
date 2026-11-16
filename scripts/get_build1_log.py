import boto3
import time

ssm = boto3.client('ssm', region_name='us-east-1')
instance_id = 'i-0f92009bba991c492'

cmds = [
    "curl -s -u admin:admin123 http://localhost:8080/job/vle9/1/consoleText"
]

r = ssm.send_command(InstanceIds=[instance_id], DocumentName='AWS-RunShellScript', Parameters={'commands': cmds}, TimeoutSeconds=60)
cmd_id = r['Command']['CommandId']
time.sleep(5)
inv = ssm.get_command_invocation(CommandId=cmd_id, InstanceId=instance_id)
print(inv.get('StandardOutputContent',''))
