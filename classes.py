import json
import paramiko

class Server:
    def __init__(self, ip):
        #username and password arent required
        #self.username = uname
        self.ip = ip
        #self.password = pwd
        
    def connect(self, b):
        self.client=paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(b.ip,22,b.username,b.password)
        except:
            print 'Either the destination is unavailable or there is something else trying to prevent this system from communicating with the remote system'
    def disconnect(self, b):
        try:
            self.client.close()
        except:
            print 'Some Error Occurred'

class Client:
    '''
    Takes the username, passwd, and ip of the system for which this object is being constructed
    ip, username, password fields are private
    
    '''
    
    #i is the ith client for which this object will be created
    def __init__(self, i):  
                
        with open(r'C:\Users\39232\Desktop\Project Files\configFileFinal.json') as data_file:
            data = json.load(data_file)
    
        
        thisSystem = data['System'+str(i)]
        thisSystemDetails = thisSystem['details']
        self.packages = thisSystem['packages']
        self.services = thisSystem['services']
        self.commands = thisSystem['commands']
        self.ip = thisSystemDetails['ip']
        self.username = thisSystemDetails['username']
        self.password = thisSystemDetails['password']
               
    
    def checkValues(self):
        print self.ip, self.username, self.password, self.packages, self.commands
    
    def serviceStatus(self,servicename):
        
        self.client=paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.ip,22,self.username,self.password)
        
        i,o,e=self.client.exec_command('net start')
    
        a = o.readlines()
        
        for line in a:
        
            if str(line).strip() == servicename:
                #print servicename, ' status : running'
                self.client.close()
                return 1
        
        #print servicename, ' status : Stopped'
        self.client.close()
        return 0
            
        
    