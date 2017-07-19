import json, os
import paramiko
from classes import *

def remoteCopy(srcComputer,destnComputer):
    
    try:
        srcComputer.connect(destnComputer)
    
        sftp = srcComputer.channel.open_sftp()
        for pkgs in destnComputer.packages:
                
            
            print('Copying Package : '+str(pkgs.name))
            src = pkgs.src
            destn = pkgs.destn
            
            print(src, destn)
            #try:
            for root, dirs, files in os.walk(src, topdown=True):
                
                print('Root directory is ',root)
                
                print('files are')
                for name in files:
                    print(name)
                    print('from source ',os.path.join(root,name))
                    print('to destn ',destn+'\\'+root.replace(src,'')+'\\'+name)
                    sftp.put(os.path.join(root,name), destn+'\\'+root.replace(src,'')+'\\'+name)
                    
                
                print('directories are')
                for name in dirs:
                    print(name)
                    sftp.mkdir(destn+'\\'+root.replace(src,'')+'\\'+name, 0777)
                    
                print('changing loop\n\n')
        
    except:
            print('\n\nError while copying')

    srcComputer.disconnect(destnComputer)

def startStopServices(srcComputer,destnComputer):
    
    
    try:
        for service in destnComputer.services:
            
            srcComputer.connect(destnComputer)
            servicename = service.name
            action = service.action
            print(servicename, ' to be ',action)
            
            if action == 'start':
                if destnComputer.serviceStatus(servicename) == 0:
                    print(servicename, ' successfully started')
                    srcComputer.channel.exec_command('net start '+servicename+' /yes')
                else:
                    print(servicename,' is already running')
            elif action == 'stop':
                if destnComputer.serviceStatus(servicename) == 1:
                    print(servicename, ' successfully stopped')
                    srcComputer.channel.exec_command('net stop '+servicename+' /yes')
                else:
                    print(servicename, ' was already stopped')
            srcComputer.disconnect(destnComputer)
    except:
        print('Error while configuring services')
    
if __name__ == '__main__':
    
    a = Server(sys.argv[2])
    #remember to create a client object for each of the destination systems
    b = Client(0)
    
    remoteCopy(a,b)
    startStopServices(a,b)
    
    
