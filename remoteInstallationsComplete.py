import paramiko, os

ip = '192.168.56.102'
username = 'IEUser'
password = 'Passw0rd!'


f = open(r'C:\Users\39232\Desktop\Project Files\installingCode.py','w')
f.write('import subprocess\n')
installationList = ['abba','jabba']


for el in installationList:
    f.write('\ntry:\n\t')
    f.write('subprocess.call(\'msiexec /i '+el+'\')\n')
    f.write('except:\n\tprint \'program '+el+' failed to execute on the remote system\'')
f.close()


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

print stdout.readlines()
print stderr.readlines()