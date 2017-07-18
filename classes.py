import sys, json
import paramiko

class Server:
    def __init__(self, ip):
        self.username = None
        self.ip = ip
        self.password = None
        self.channel = None
        print 'ip is ',self.ip,'\n\n\n\n'
        
    def connect(self, b):
        self.channel=paramiko.SSHClient()
        self.channel.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.channel.connect(b.ip,22,b.username,b.password)
        except:
            print 'Either the destination is unavailable or there is something else trying to prevent this system from communicating with the remote system'
    def disconnect(self, destnComputer):
        try:
            self.channel.close()
        except:
            print 'Some Error Occurred'

class Client:
    '''
    Takes the username, passwd, and ip of the system for which this object is being constructed
    ip, username, password fields are private
    
    '''
    
    #i is the ith client for which this object will be created
    def __init__(self, i):  
                
        self.channel = None     #a channel to the same system which this object will denote
        with open(sys.argv[1]) as data_file:
            data = json.load(data_file)
    
        
        thisSystem = data[i]
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
        
        self.channel=paramiko.SSHClient()
        self.channel.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.channel.connect(self.ip,22,self.username,self.password)
        
        i,o,e=self.channel.exec_command('net start')
    
        a = o.readlines()
        
        for line in a:
        
            if str(line).strip() == servicename:
                #print servicename, ' status : running'
                self.channel.close()
                return 1
        
        #print servicename, ' status : Stopped'
        self.channel.close()
        return 0
            
        
    