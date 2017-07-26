from classes import *
from parsingMain import *
import sys
from functionalities import *
import datetime


if __name__ == '__main__':
    logFile = open('deploymentLog'\
    +str(str((datetime.datetime.now())).replace(':','-').replace('.','-').replace(' ','-'))+'.txt', 'w')
    #a log file is created with name containing the date and time of when this program will be executed
    
    #invalid usage clause    
    if len(sys.argv) != 3:
        print 'Usage : python main.py <Full path for the configuration file> <deploying server\' ip address>'
        sys.exit()
    
    #the configuration file is present on the disk. parsingFromDisk(...) reads that file, parses the data
    #in the form a dictionary and return the data with the name 'configFileData'
    configFileData = parsingFromDisk(sys.argv[1], logFile)   
    
    #srvr refers to the system from which the installations have to take place
    srvr = Server(sys.argv[2], logFile)
    
    #remember, we must create a client object for each of the destination systems
    #and repeat the functionalities for each of the client systems, as is done here
    #for client0
    client0 = Client(configFileData, '192.168.56.101', logFile)
    
    #calling each of the functionalities
    deploy(srvr, client0, logFile)
    startStopServices(srvr, client0, logFile)
    remoteInstallation(srvr,client0, logFile)