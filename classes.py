import sys
import json
import time
import paramiko
from parsing import *

class Machine:

    def __init__(self, ip, uname=None, pwd=None):
        self.ip = ip
        self.username = uname
        self.password = pwd
        self.channel = None

    def connect(self, destn):
        self.channel=paramiko.SSHClient()
        self.channel.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.channel.connect(destn.ip, 22, destn.username, destn.password)
    
    def disconnect(self, destn):
        try:
            self.channel.close()
        except:
            print('Some Error Occurred while disconnecting')
    

class Server(Machine):
    def __init__(self, ip):
        Machine.__init__(self, ip)
            
class Client(Machine):
    '''Takes the username, passwd, and ip of the system for which this object is being constructed
    '''
   
    def __init__(self, clientIndex):  
        self.packages = []        
        self.services = []
        self.msis = []
        self, ip, uname, pwd = parsing(self, clientIndex, sys.argv[1])
        Machine.__init__(self, ip, uname, pwd)
        print('start of client constructor\n')
        print('destn system is :',self.ip, self.username, self.password)
        print('end of client constructor\n')
                                                                                                                                                                                                                                                                                                                                                                                                                         
    def checkValues(self):
        print(self.ip, self.username, self.password, self.packages, self.commands)
    
    def serviceStatus(self, servicename):
        self.channel=paramiko.SSHClient()
        self.channel.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.channel.connect(self.ip, 22, self.username, self.password)
        
        i, o, e=self.channel.exec_command('net start')
        a = o.readlines()
        for line in a:
            if str(line).strip() == servicename:
                self.channel.close()
                return 1
        self.channel.close()
        return 0
            