import paramiko

def status(a):
    ip = '192.168.56.102'
    username = 'IEUser' 
    password = 'Passw0rd!'
    servicename = 'Server'
    
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,22,username,password)
    
    i,o,e=ssh.exec_command('net start')
    
    a = o.readlines()
    
    for line in a:
        print str(line).strip()
        if str(line).strip() == servicename:
            print line, 'Running'
            return 1
    
    print 'Stopped'
    
    return 0    
    
    #there is an error with this Y input, it says socket is closed. Whereas 
    ssh.close()
