import paramiko
from fetchClientDetails import *

#the superclass which contains common attributes of both client and server
class Machine:

    def __init__(self, ip, uname=None, pwd=None):
        self.ip = ip
        self.username = uname
        self.password = pwd
        self.channel = None 
        '''
        channel is not required for client systems
        it is an attribute which will be used only by the server object
        '''
    
    def connect(self, destn, logFile):
        '''
        connect() establishes an ssh connection to client object 'destn' using paramiko module
        connect() takes extra argument logFile for logging purpose
                
        NOTE: connect sets an attribute 'channel' as the SSHClient connection to the destn.
        All operations from the server to the client systems will occur by :
        <server_object>.channel.<operation>(<client_object>)
        '''
        try:
            self.channel=paramiko.SSHClient()
            self.channel.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.channel.connect(destn.ip, 22, destn.username, destn.password)
            #using ip, username and password of destn system, we've established an ssh connection
        
        except Exception as e:
            print 'Error while connecting to ',destn.ip
            logFile.write('\nError Occurred while connecting\n'+str(e))
    
    def disconnect(self, destn, logFile):
        #disconnect() closes the ssh connection to 'destn' system
        try:
            self.channel.close()
        except Exception as e:
            print('Error Occurred while disconnecting')
            logFile.write('\nError Occurred while disconnecting\n'+str(e))
    

class Server(Machine):
    #Server refers to the system from which the installations have to take place

    def __init__(self, ip, logFile):
        #this constructor takes the IP and the file descriptor of the log file as input
        Machine.__init__(self, ip)
        #for server object, only IP is required, rest all fields are not required at all
            

class Client(Machine):
    
    def __init__(self, configFileData, clientIP, logFile):  
        '''
        this constructor takes configFileData (see main.py for its description),
        the IP address of the destined client, and logFile as arguments
        '''
        self.packages = []      #a list that will hold all packages to be deployed on this client
        self.services = []      #a list that will hold all services to be configured on this client
        self.msis = []          #a list that will hold all msis to be installed on this client
        '''
        NOTE : The current version of the code allows installation of files in msi format only.
        Other file formats fail to install
        '''
        ip = clientIP
        
        '''
        fetchClientDetails() reads the dictionary configFileData and pulls out the
        packages, msis, services, to be deployed on the client with ip=clientIP
        it also returns the username, and password of the local admin
        on the client system after reading them from the dictionary
        '''
        self, uname, pwd = fetchClientDetails(self, configFileData, clientIP, logFile)
        '''
        call the parent constructor to assign the ip, username, and password
        there was no need to assign the ip again though :P
        '''
        Machine.__init__(self, ip, uname, pwd)
        
        #logging details
        logFile.write('\nClient '+str(clientIP)+' constructor started from classes.py file')
        logFile.write('\ndestn system is :'+str(self.ip)+str(self.username)+str(self.password))
        logFile.write('\nend of client constructor from classes.py\n')
        print('destn system is :',self.ip, self.username, self.password)
                                                                                                                                                                                                                                                                                                                                                                                                                         
    
    def serviceStatus(self, servicename):
        '''
        serviceStatus() takes in the name of a service, and returns 1 if the service is already
        running on the client denoted by this object, else returns 0
        '''
        self.channel=paramiko.SSHClient()
        self.channel.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        '''
        to find the service status, the client need to establish a connection to itself,
        then read the services currently running on it, and return 1 or 0 accordingly
        
        NOTE: this is the only place in our whole scenario where a Client object itself is establishing
        a connection to itself. All other places, Server object establishes a connection to Client object
        and performs any operation on the client using <Server_object>.channel.<operation>(<Client_object>)
        '''
        self.channel.connect(self.ip, 22, self.username, self.password)
        
        i, o, e=self.channel.exec_command('net start')
        services = o.readlines()
        
        #each line in services is the name of a service currently running
        for line in services: 
            if str(line).strip().lower() == servicename.lower():
                self.channel.close()
                return 1
        self.channel.close()
        return 0
            