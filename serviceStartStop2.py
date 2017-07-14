import paramiko

ip = '192.168.56.102'
username = 'IEUser' 
password = 'Passw0rd!'
command = 'net stop server'

cmd='net start server' 

ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip,22,username,password)

#i = open(r'C:\Users\39232\Desktop\command.txt','r')
#i.write('Y')

i,o,e=ssh.exec_command(cmd)
#while 1:
i.write('Y\n')
i.flush()

a = o.readlines()

for line in a:
    print line

print e.read()

#there is an error with this Y input, it says socket is closed. Whereas 
ssh.close()
