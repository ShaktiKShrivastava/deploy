import os
from classes import *
import random
import string

#if at least one package fails, all the packages will fail and no package will be copied
def deploy(srcComputer, destnComputer, logFile):
    try:
        srcComputer.connect(destnComputer, logFile)
        sftp = srcComputer.channel.open_sftp()
        logFile.write('\n------------Copying packages started------------\n')
        for pkgs in destnComputer.packages:
            remoteCopy(sftp, pkgs, logFile)
        sftp.close()
        srcComputer.disconnect(destnComputer, logFile)
        logFile.write('\n------------Copying packages ended------------\n')
    except Exception as e:
        print('Error while deploying packages!')
        logFile.write('\nError from deploy function in functionalities.py file\n'+str(e))
            

def remoteCopy(sftp, pkgs, logFile):
    try:
        error = ''
        print('Copying Package : '+str(pkgs.name))
        logFile.write('\nCopying Package : '+str(pkgs.name))
        src = pkgs.src
        destn = pkgs.destn
        print(src, destn)
        
        directories_present_on_destn = sftp.listdir(destn[:destn.rfind('\\')])
        for line in directories_present_on_destn:
            if destn[destn.rfind('\\')+1:] == line:
                error = 'A directory with '+destn[destn.rfind('\\')+1:]+' already exists' 
                logFile.write('\nError while copying : '+error)
                raise Exception
                
        sftp.mkdir(destn)
        for root, dirs, files in os.walk(src, topdown=True):
            logFile.write('\nCurrent root directory is '+str(root))
            
            for name in files:
                #print(name)
                logFile.write('\nfrom source '+str(os.path.join(root,name)))
                logFile.write('\nto destn '+destn+'\\'+root.replace(src,'')+'\\'+name)
                sftp.put(os.path.join(root, name), destn+'\\'+root.replace(src,'')+'\\'+name)
            #print('directories are')
            
            for name in dirs:
                #print(name)
                sftp.mkdir(destn+'\\'+root.replace(src,'')+'\\'+name, 0777)
                logFile.write('\nCreated directory '+destn+'\\'+root.replace(src,'')+'\\'+name+' at remote system')
        logFile.write('\nCopying Packages completed successfully')
                
    except Exception as e:
        print('Error while deploying package ',pkgs,'\nError : ',error)
        logFile.write('\nError while deploying package '+str(pkgs.name)+'\nError : '+error+'\n'+str(e))

def startStopServices(srcComputer, destnComputer, logFile):
    logFile.write('\n------------Configuring services started------------\n')
    try:
        for service in destnComputer.services:
            srcComputer.connect(destnComputer, logFile)
            servicename = service.name
            action = service.action
            print(servicename, ' to be ', action)
            logFile.write('\n'+servicename+' to be '+action)
            
            if action == 'start':
                if destnComputer.serviceStatus(servicename) == 0:
                    print(servicename, ' successfully started')
                    logFile.write('\n'+servicename+' successfully started')        
                    srcComputer.channel.exec_command('net start '+servicename+' /yes')
                    #srcComputer has the channel open to the destnComputer, hence srcComputer.channel.exec_command(...)
                else:
                    print(servicename,' is already running')
                    logFile.write('\n'+servicename+' is already running')
            
            elif action == 'stop':
                if destnComputer.serviceStatus(servicename) == 1:
                    print(servicename, ' successfully stopped')
                    logFile.write('\n'+servicename+' successfully stopped')
                    srcComputer.channel.exec_command('net stop '+servicename+' /yes')
                else:
                    print(servicename, ' was already stopped')
                    logFile.write('\n'+servicename+' was already stopped')
            srcComputer.disconnect(destnComputer, logFile)
        logFile.write('\n------------Configuring sevices completed------------\n')
            
    except Exception as e:
        print('Error while configuring services')
        logFile.write('\nError while configuring services, from function startStopServices in functionalities.py file\n'+str(e))


def preCopy(srcComputer, destnComputer, logFile):
    #return the path to the temporary directory created
    try:
        print('copying files for installation started')
        logFile.write('\nCopying files for installation started')
        srcComputer.connect(destnComputer, logFile)
        sftp = srcComputer.channel.open_sftp()
        temp = ''.join(random.choice(string.ascii_uppercase) for _ in range(16))

        sftp.mkdir('C:\\Users\\Public\\'+temp)
        logFile.write('\nMaking a temporary directory C:\\Users\\Public\\'+temp)
        
        for msi in destnComputer.msis:
            path = msi.path
            sftp.put(path, r'C:\\Users\\Public\\'+temp+'\\'+str(msi.path[msi.path.rfind('\\')+1:]))
            logFile.write('\nCopied the msi '+path)
        
        logFile.write('\nWriting the python script for installation')
        f = open(r'C:\Users\39232\Desktop\Project Files\installingCode.py','w')
        f.write('import subprocess, time\n')
        
        for msi in destnComputer.msis:
            f.write('\na = subprocess.call(r\'msiexec /i '+r'C:\\Users\\Public\\'+temp+'\\'+str(msi.path[msi.path.rfind('\\')+1:])+'\')\n')
            #f.write('time.sleep(2)\n')
            f.write('if a!=0:\n\tprint\''+str(msi.path[msi.path.rfind('\\')+1:])+' failed to execute on the remote system\'\n')
            f.write('else:\n\tprint\''+str(msi.path[msi.path.rfind('\\')+1:])+' successfully installed on the remote system\'\n')
        f.close()
        logFile.write('\nCompleted the python script for installation')
        
        sftp.put(r'C:\Users\39232\Desktop\Project Files\installingCode.py', r'C:\\Users\Public\\'+temp+'\\installingCode.py')
        logFile.write('\nCopied the python script for installation to client')
        
        sftp.close()
        srcComputer.disconnect(destnComputer, logFile)
        print('Copying files for installation ended')
        return 'C:\\Users\\Public\\'+temp
        logFile.write('\nCopying files for installation ended')
        
    except Exception as e:
        print('copying msis to the remote system for installation failed')
        logFile.write('\nPrecopy failed, from function precopy in functionalities.py, Error : \n'+str(e))
        
        
def triggerMSIs(srcComputer, destnComputer, path, logFile):
    try:
        pathnew = path.replace('\\','/')
        srcComputer.connect(destnComputer, logFile)
        print('installations started')
        logFile.write('\ninstallations started on client')
        
        stdin, stdout, stderr = srcComputer.channel.exec_command(r'C:/Python27/python '+pathnew+'/installingCode.py')
        output = stdout.readlines()
        error = stderr.readlines()
        if len(error) > 0:
            print('Error in excuting msis : ',error)
            logFile.write('\nError in excuting msis : '+error)
        
        logFile.write('\n')
        for line in output:
            print(line)
            logFile.write(line)
            
        srcComputer.disconnect(destnComputer, logFile)
        print('installations ended')
        logFile.write('\ninstallations ended')
    except Exception as e:
        print('Could not trigger msi on the remote system, installation failed')
        logFile.write('\nFrom function triggerMSIs in functionalities.py file : installation failed, error : \n'+str(e))
        

def removeCopiedFiles(srcComputer, destnComputer, path, logFile):
    try:
        print('removing the copied msis')
        logFile.write('\nremoving the copied msi files')
        
        srcComputer.connect(destnComputer, logFile)
        sftp = srcComputer.channel.open_sftp()
        filesInDestnSystem = sftp.listdir(path)

        for files in filesInDestnSystem:
            sftp.remove(path+'\\'+files)
            logFile.write('\nremoved '+path+'\\'+files)
        sftp.rmdir(path)
        logFile.write('\nRemoving the temporary directory '+path)
        
        sftp.close()
        srcComputer.channel.close()
        print('removing successful')
        logFile.write('\nSuccessfully removed the temporary directory')
               
    except Exception as e:
        print('removing copied files failed')
        logFile.write('\nFrom function removeCopiedFiles in functionalities.py file, Error : '+str(e))
        

def remoteInstallation(srcComputer, destnComputer, logFile):
    logFile.write('\n------------Installations Started------------\n')
    path = preCopy(srcComputer, destnComputer, logFile)
    triggerMSIs(srcComputer, destnComputer, path, logFile)
    removeCopiedFiles(srcComputer, destnComputer, path, logFile)
    logFile.write('\n------------Installations Ended------------\n')