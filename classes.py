import paramiko
from fetchClientDetails import *

class Machine:

    def __init__(self, ip, uname=None, pwd=None):
        self.ip = ip
        self.username = uname
        self.password = pwd
        self.channel = None

    def connect(self, destn, logFile):
        try:
            self.channel=paramiko.SSHClient()
            self.channel.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.channel.connect(destn.ip, 22, destn.username, destn.password)
        except Exception as e:
            print 'Error while connecting to ',destn.ip
            logFile.write('\nError Occurred while connecting\n'+str(e))
            
    def disconnect(self, destn, logFile):
        try:
            self.channel.close()
        except Exception as e:
            print('Error Occurred while disconnecting')
            logFile.write('\nError Occurred while disconnecting\n'+str(e))
    

class Server(Machine):
    def __init__(self, ip, logFile):
        Machine.__init__(self, ip)
            
class Client(Machine):
    '''Takes the username, passwd, and ip of the system for which this object is being constructed
    '''
   
    def __init__(self, configFileData, clientIP, logFile):  
        self.packages = []        
        self.services = []
        self.msis = []
        ip = clientIP
        self, uname, pwd = fetchClientDetails(self, configFileData, clientIP, logFile)
        Machine.__init__(self, ip, uname, pwd)
        logFile.write('\nClient '+str(clientIP)+' constructor started from classes.py file')
        logFile.write('\ndestn system is :'+str(self.ip)+str(self.username)+str(self.password))
        logFile.write('\nend of client constructor from classes.py\n')
        print('destn system is :',self.ip, self.username, self.password)
                                                                                                                                                                                                                                                                                                                                                                                                                         
    
    def serviceStatus(self, servicename):
        self.channel=paramiko.SSHClient()
        self.channel.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.channel.connect(self.ip, 22, self.username, self.password)
        
        i, o, e=self.channel.exec_command('net start')
        a = o.readlines()
        for line in a:
            if str(line).strip().lower() == servicename.lower():
                self.channel.close()
                return 1
        self.channel.close()
        return 0
            