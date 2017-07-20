import paramiko, os
import subprocess

ip = '192.168.56.101'
username = 'IEUser'
password = 'Passw0rd!'


f = open(r'C:\Users\39232\Desktop\Project Files\installingCode.py','w')
f.write('import subprocess, time\n')
installationList = [r'C:\Users\Public\Exp\shakti_kumar.msi','jabba']


for el in installationList:
    #f.write('\ntry:\n\t')
    f.write('\na = subprocess.call(r\'msiexec /i '+el+'\')\n')
    f.write('time.sleep(2)\n')
    f.write('if a!=0:\n\tprint\''+el+' failed to execute on the remote system\'\n')
    f.write('else:\n\tprint\''+el+' successfully installed on the remote system\'\n')
f.close()

#subprocess.call(r'python "C:\Users\39232\Desktop\Project Files\installingCode.py"')


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(ip, 22, username, password)

sftp = client.open_sftp()
sftp.put(r'C:\Users\39232\Desktop\Project Files\installingCode.py', r'C:\Users\Public\Exp\installingCode.py')
client.close()

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(ip, 22, username, password)

stdin, stdout, stderr = client.exec_command(r'C:/Python27/python C:/Users/Public/Exp/installingCode.py')

output = stdout.readlines()
error = stderr.readlines()
if len(error) > 0:
    print 'Error in excuting msis'
for line in output:
    print line