import json, os
import paramiko
from classes import *

def remoteCopy(a,b):
    
    a.connect(b)
    
    sftp = a.client.open_sftp()
    for p in b.packages:
            
        
        print a
        src = str(p['source'])
        destn = str(p['destn'])
        
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

    a.disconnect(b)

def startStopServices(a,b):
    
    
    
    for service in b.services:
        
        a.connect(b)
        servicename = str(service['name'])
        action = str(service['action'])
        print servicename, ' to be ',action
        
        if action == 'start':
            if b.serviceStatus(servicename) == 0:
                print servicename, ' successfully started'
                a.client.exec_command('net start '+servicename+' /yes')
            else:
                print servicename,' is already running'
        elif action == 'stop':
            if b.serviceStatus(servicename) == 1:
                print servicename, ' successfully stopped'
                a.client.exec_command('net stop '+servicename+' /yes')
            else:
                print servicename, ' was already stopped'
        a.disconnect(b)
        
    
if __name__ == '__main__':
    
    a = Server('192.168.56.1')
    b = Client(1)
    
    remoteCopy(a,b)
    startStopServices(a,b)
    
    
