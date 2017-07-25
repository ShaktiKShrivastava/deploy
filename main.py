from classes import *
from parsingMain import *
import sys
from functionalities import *
import datetime


if __name__ == '__main__':
    logFile = open('deploymentLog'\
    +str(str((datetime.datetime.now())).replace(':','-').replace('.','-').replace(' ','-'))+'.txt', 'w')

        
    if len(sys.argv) != 3:
        print 'Usage : python main.py <Full path for the configuration file> <deploying server\' ip address>'
        sys.exit()

    configFileData = parsingFromDisk(sys.argv[1], logFile)   #parsing of the configFile from the disk done
    
    srvr = Server(sys.argv[2], logFile)
    #remember to create a client object for each of the destination systems
    client0 = Client(configFileData, '192.168.56.101', logFile)
    deploy(srvr, client0, logFile)
    startStopServices(srvr, client0, logFile)
    remoteInstallation(srvr,client0, logFile)