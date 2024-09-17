import paramiko
host = "xxx-01-r06esx44.xxx.com"
user ="root"
password ="xxxxx"
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
client.connect(hostname=host, port=22, username=user,password=password,look_for_keys=False)

print(" ")
print("Managemenet agtents status of ESXi:" + host)
print(" ")
#Get vpxa service status
stdin, stdout, stderr = client.exec_command('/etc/init.d/vpxa status')
vpxa_status = stdout.read()
print(vpxa_status.decode('utf-8'))

#Restart vpxa service
stdin, stdout, stderr = client.exec_command('/etc/init.d/vpxa restart')
print(stdout.read().decode('utf-8'))

#Get hostd service status
stdin, stdout, stderr = client.exec_command('/etc/init.d/hostd status')
hostd_status = stdout.read()
print(hostd_status.decode('utf-8'))

#Restart hostd service
stdin, stdout, stderr = client.exec_command('/etc/init.d/hostd restart')
print(stdout.read().decode('utf-8'))

client.close()
del client, stdin, stdout, stderr
