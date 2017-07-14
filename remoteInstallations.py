import paramiko, os


#just change this line
UbuntuOrWindows = 2



ip1='192.168.56.101'
username1='osboxes'
password1='osboxes.org'

ip2='192.168.56.102'
username2='IEUser'
password2='Passw0rd!'




cmd=r'C:/Users/Public/Exp/shakti_kumar.msi'

if UbuntuOrWindows == 1:
    ip = ip1
    username = username1
    password = password1
else:
    ip = ip2
    username = username2
    password = password2
    
ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip,22,username,password)
'''
channel = ssh.invoke_shell()
print ("Logged in into Site server")
channel.send("C:/Program\ Files/OpenSSH/testing.sh")

print ("Script executed perfectly")
ssh.close()
'''



stdin, stdout, stderr = ssh.exec_command(r'C:/Python27/python C:/Python27/testing.py')
#stdin, stdout, stderr = ssh.exec_command(r'msiexec /i C:/Users/Public/Exp/shakti_kumar.msi')



for line in stdout.readlines():
    print line
print stderr.readlines()

#there is an error with this Y input, it says socket is closed. Whereas 
ssh.close()
