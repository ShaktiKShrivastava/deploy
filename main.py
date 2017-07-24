import os
from classes import *
from parsingMain import *
import random
import string
import sys

#if at least one package fails, all the packages will fail and no package will be copied
def remoteCopy(srcComputer, destnComputer):
    try:
        error = ''
        srcComputer.connect(destnComputer)
        sftp = srcComputer.channel.open_sftp()
        for pkgs in destnComputer.packages:
            print('Copying Package : '+str(pkgs.name))
            src = pkgs.src
            destn = pkgs.destn
            print(src, destn)
            
            directories_present_on_destn = sftp.listdir(destn[:destn.rfind('\\')])
            for line in directories_present_on_destn:
                if destn[destn.rfind('\\')+1:] == line:
                    error = 'A directory with '+destn[destn.rfind('\\')+1:]+' already exists' 
                    raise Exception
                    
            sftp.mkdir(destn)
            for root, dirs, files in os.walk(src, topdown=True):
                print('Root directory is ',root)
                print('files are')
                
                for name in files:
                    print(name)
                    print('from source ',os.path.join(root,name))
                    print('to destn ', destn+'\\'+root.replace(src,'')+'\\'+name)
                    sftp.put(os.path.join(root, name), destn+'\\'+root.replace(src,'')+'\\'+name)
                print('directories are')
                
                for name in dirs:
                    print(name)
                    sftp.mkdir(destn+'\\'+root.replace(src,'')+'\\'+name, 0777)
                    
                print('changing loop\n\n')
        sftp.close()
        srcComputer.disconnect(destnComputer)
        
    except:
            print('\n\nError while copying packages\n')
            print(error)
    

def startStopServices(srcComputer, destnComputer):
    try:
        for service in destnComputer.services:
            srcComputer.connect(destnComputer)
            servicename = service.name
            action = service.action
            print(servicename, ' to be ', action)
            if action == 'start':
                if destnComputer.serviceStatus(servicename) == 0:
                    print(servicename, ' successfully started')
                    srcComputer.channel.exec_command('net start '+servicename+' /yes')
                    #srcComputer has the channel open to the destnComputer, hence srcComputer.channel.exec_command(...)
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


def preCopy(srcComputer, destnComputer):
    #return the path to the temporary directory created
    try:
        print('copying files for installation started')
        srcComputer.connect(destnComputer)
        sftp = srcComputer.channel.open_sftp()
        temp = ''.join(random.choice(string.ascii_uppercase) for _ in range(16))

        sftp.mkdir('C:\\Users\\Public\\'+temp)
        
        for msi in destnComputer.msis:
            path = msi.path
            sftp.put(path, r'C:\\Users\\Public\\'+temp+'\\'+str(msi.path[msi.path.rfind('\\')+1:]))
        
        f = open(r'C:\Users\39232\Desktop\Project Files\installingCode.py','w')
        f.write('import subprocess, time\n')
        
        for msi in destnComputer.msis:
            f.write('\na = subprocess.call(r\'msiexec /i '+r'C:\\Users\\Public\\'+temp+'\\'+str(msi.path[msi.path.rfind('\\')+1:])+'\')\n')
            #f.write('time.sleep(2)\n')
            f.write('if a!=0:\n\tprint\''+str(msi.path[msi.path.rfind('\\')+1:])+' failed to execute on the remote system\'\n')
            f.write('else:\n\tprint\''+str(msi.path[msi.path.rfind('\\')+1:])+' successfully installed on the remote system\'\n')
        f.close()
        
        sftp.put(r'C:\Users\39232\Desktop\Project Files\installingCode.py', r'C:\\Users\Public\\'+temp+'\\installingCode.py')
        sftp.close()
        srcComputer.disconnect(destnComputer)
        print('Copying files for installation ended')
        return 'C:\\Users\\Public\\'+temp
        
    except:
        print('copying msis to the remote system for installation failed')
        

def triggerMSIs(srcComputer, destnComputer, path):
    try:
        pathnew = path.replace('\\','/')
        srcComputer.connect(destnComputer)
        print('installations is started')
        stdin, stdout, stderr = srcComputer.channel.exec_command(r'C:/Python27/python '+pathnew+'/installingCode.py')
        output = stdout.readlines()
        error = stderr.readlines()
        if len(error) > 0:
            print('Error in excuting msis : ',error)
        for line in output:
            print(line)
        srcComputer.disconnect(destnComputer)
        print('installations ended')
    except:
        print('Could not trigger msi on the remote system, installation failed')


def removeCopiedFiles(srcComputer, destnComputer, path):
    try:
        print('removing the copied msis')
        srcComputer.connect(destnComputer)
        sftp = srcComputer.channel.open_sftp()
        filesInDestnSystem = sftp.listdir(path)

        for file in filesInDestnSystem:
            sftp.remove(path+'\\'+file)
        sftp.rmdir(path)
        sftp.close()
        srcComputer.channel.close()
        print('removing successful')
    except:
        print('removing copied files failed')
        

def remoteInstallation(srcComputer, destnComputer):
    path = preCopy(srcComputer, destnComputer)
    triggerMSIs(srcComputer, destnComputer, path)
    removeCopiedFiles(srcComputer, destnComputer, path)    

if __name__ == '__main__':
    
    configFileData = parsingFromDisk(sys.argv[1])   #parsing of the configFile from the disk done
    
    srvr = Server(sys.argv[2])
    #remember to create a client object for each of the destination systems
    client0 = Client(configFileData, '192.168.56.101')
    remoteCopy(srvr, client0)
    startStopServices(srvr, client0)
    remoteInstallation(srvr,client0)
    srvr.disconnect(client0)
