import paramiko

ip = '192.168.56.102'
username = 'IEUser' 
password = 'Passw0rd!'
command = 'start'
servicename = 'OpenSSH Server'

ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip,22,username,password)

i,o,e=ssh.exec_command('net start')

a = o.readlines()
l = 0
for line in a:
    if str(line).find(servicename) != -1:
        print line, 'Running'
        l = 1

if l == 0:
    print 'Stopped'

i,o,e=ssh.exec_command('net start OpenSSH Server')


print o.read()
print e.read()
print e.read()

#there is an error with this Y input, it says socket is closed. Whereas 
ssh.close()
