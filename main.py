import json, os
import paramiko
from classes import *

def remoteCopy(srcComputer,destnComputer):
    
    srcComputer.connect(destnComputer)
    
    sftp = srcComputer.client.open_sftp()
    for pkgs in destnComputer.packages:
            
        
        print srcComputer
        src = str(pkgs['source'])
        destn = str(pkgs['destn'])
        
        print src, destn
        
        
        try:
            
            for root, dirs, files in os.walk(src, topdown=True):
                
                print root
                print 'this is the root',root
                
                print 'files are'
                for name in files:
                    print name
                    print 'from source ',os.path.join(root,name)
                    print 'to destn ',destn+'\\'+root.replace(src,'')+'\\'+name
                    sftp.put(os.path.join(root,name), destn+'\\'+root.replace(src,'')+'\\'+name)
                    
                
                print 'dirs are'
                for name in dirs:
                    print name
                    sftp.mkdir(destn+'\\'+root.replace(src,'')+'\\'+name, 0777)
                    
                print 'changing loop\n\n'
        
        except:
            print '\n\nError while copying, the values retrived at error point were'
            print 'destn : ',destn,' root : ',root, 'name : ',name

    srcComputer.disconnect(destnComputer)

def startStopServices(srcComputer,destnComputer):
    
    
    
    for service in destnComputer.services:
        
        srcComputer.connect(destnComputer)
        servicename = str(service['name'])
        action = str(service['action'])
        print servicename, ' to be ',action
        
        if action == 'start':
            if destnComputer.serviceStatus(servicename) == 0:
                print servicename, ' successfully started'
                srcComputer.client.exec_command('net start '+servicename+' /yes')
            else:
                print servicename,' is already running'
        elif action == 'stop':
            if destnComputer.serviceStatus(servicename) == 1:
                print servicename, ' successfully stopped'
                srcComputer.client.exec_command('net stop '+servicename+' /yes')
            else:
                print servicename, ' was already stopped'
        srcComputer.disconnect(destnComputer)
        
    
if __name__ == '__main__':
    
    a = Server(sys.argv[2])
    b = Client(0)
    
    remoteCopy(a,b)
    startStopServices(a,b)
    
    
