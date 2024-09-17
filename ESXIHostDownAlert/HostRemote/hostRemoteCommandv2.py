import paramiko
host = "xxx-r01esx29xxxx.com"
user ="root"
password ="xxxx"
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
client.connect(hostname=host, port=22, username=user,password=password,look_for_keys=False)

#Get vpxa service status
#stdin, stdout, stderr = client.exec_command("for name in `vmkchdev -l | grep vmhba | awk '{print$5}'`;do echo $name ; echo 'VID :DID  SVID:SDID'; vmkchdev -l | grep $name | awk '{print $2 , $3}';printf 'Driver: ';echo `esxcfg-scsidevs -a | grep $name |awk '{print $2}'`;vmkload_mod -s `esxcfg-scsidevs -a | grep $name|awk '{print $2}'` |grep -i version;echo `lspci -vvv | grep $name | awk '{print $1=$NF="",$0}'`;printf '\n';done")
stdin, stdout, stderr = client.exec_command("nsxdp-cli vswitch mac-learning get -dvs xxx-xx-vc49-dvs")
#stdin, stdout, stderr = client.exec_command("nsxdp-cli vswitch mac-learning set --learn-static -dvs sc1-04-vc49-dvs")
CLOMD_status = stdout.read()
print(f'Result from {host}')
print(CLOMD_status.decode('utf-8'))

# #Restart vpxa service
# stdin, stdout, stderr = client.exec_command('/etc/init.d/clomd start')
# print(stdout.read().decode('utf-8'))

# #Get hostd service status
# # stdin, stdout, stderr = client.exec_command('/etc/init.d/clomd restart')
# # print(stdout.read().decode('utf-8'))

# #Restart hostd service
# stdin, stdout, stderr = client.exec_command('/etc/init.d/clomd status')
# CLOMD_status = stdout.read()
# print(CLOMD_status.decode('utf-8'))

client.close()
del client, stdin, stdout, stderr
