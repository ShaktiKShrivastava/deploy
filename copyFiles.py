import paramiko, os
client1 = paramiko.SSHClient()

#to automatically add the unknown hosts to the list of hosts supported by paramiko

'''
The default behavior with an SSHClient object is to refuse to connect to a host 
(''paramiko.RejectPolicy'') who does not have a key stored in your local ''known_hosts'' 
file. This can become annoying when working in a lab environment where machines come and
go and have the operating system reinstalled constantly.

Setting the host key policy takes one method call to the ssh client object 
(''set_missing_host_key_policy()''), which sets the way you want to manage inbound host keys. 
If you're lazy like me, you pass in the ''paramiko.AutoAddPolicy()'' which will auto-accept unknown keys.
'''
client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client1.connect('192.168.56.102', username='IEUser', password='Passw0rd!')
sftp = client1.open_sftp()



sftp.put(r'C:\Users\39232\Desktop\shakti_kumar.msi', r'C:\Users\Public\Exp\shakti_kumar.msi')
sftp.put(r'C:\Users\39232\Desktop\cab1.cab', r'C:\Users\Public\Exp\cab1.cab')


print client1
client1.close()

print client1