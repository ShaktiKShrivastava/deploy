import os
from classes import *
import random
import string

def deploy(srcComputer, destnComputer, logFile):
    #deploy copies each package as mentioned in the destnComputer.packages list to the destnComputer

    try:
        #open an ssh connection to the destnComputer. Note that this channel is an attribute of srcComputer
        srcComputer.connect(destnComputer, logFile)
        
        #open an sftp channel through the ssh connection the srcCompuetr has already opened to the client
        sftp = srcComputer.channel.open_sftp()
        
        logFile.write('\n------------Copying packages started------------\n')
        
        #call remoteCopy() for each of the packages
        for pkgs in destnComputer.packages:
            remoteCopy(sftp, pkgs, logFile)
        
        #close the sftp channel and disconnect ssh from the destnComputer
        sftp.close()
        srcComputer.disconnect(destnComputer, logFile)
        
        logFile.write('\n------------Copying packages ended------------\n')
    
    except Exception as e:
        print('Error while deploying packages!')
        logFile.write('\nError from deploy function in functionalities.py file\n'+str(e))
            
            
def remoteCopy(sftp, pkgs, logFile):
    '''
    remoteCopy() is called for each package which needs to be copied to the destnComputer
    the packages that need to be copied to the destnComputer resides in a list called destnComputer.packages
    '''
    
    try:
        error = ''
        print('Copying Package : '+str(pkgs.name))
        logFile.write('\nCopying Package : '+str(pkgs.name))
        
        #destnComputer.pacakages is a list containing object of class Package.
        #Refer fetchClientDetails.py file for attributes of class Package
        src = pkgs.src
        destn = pkgs.destn
        print(src, destn)
        
        directories_present_on_destn = sftp.listdir(destn[:destn.rfind('\\')])
        for line in directories_present_on_destn:
            if destn[destn.rfind('\\')+1:] == line:
                #if a directory with the same path as this package's destination 
                #already exists, skip this package and log this event
                error = 'A directory with '+destn[destn.rfind('\\')+1:]+' already exists' 
                logFile.write('\nError while copying : '+error)
                raise Exception
        
        #otherwise create a directory with the package's destination, and copy
        #all the files and subdirectories into it.
        sftp.mkdir(destn)
        
        #Copying is done using a top down traversal of the directory structure,
        #copying files and creating subdirectories
        for root, dirs, files in os.walk(src, topdown=True):
            logFile.write('\nCurrent root directory is '+str(root))
            
            #files has list of files in the current root directory
            for name in files:
                logFile.write('\nfrom source '+str(os.path.join(root,name)))
                logFile.write('\nto destn '+destn+'\\'+root.replace(src,'')+'\\'+name)
                sftp.put(os.path.join(root, name), destn+'\\'+root.replace(src,'')+'\\'+name)
            
            #dirs is the list of directories in the current root directory
            for name in dirs:
                sftp.mkdir(destn+'\\'+root.replace(src,'')+'\\'+name, 0777)
                logFile.write('\nCreated directory '+destn+'\\'+root.replace(src,'')+'\\'+name+' at remote system')
        
        logFile.write('\nCopying Packages completed successfully')
                
    except Exception as e:
        print('Error while deploying package ',pkgs,'\nError : ',error)
        logFile.write('\nError while deploying package '+str(pkgs.name)+'\nError : '+error+'\n'+str(e))


def startStopServices(srcComputer, destnComputer, logFile):
    '''
    startStopServices() establishes a connection to the destnComputer, and then reads
    the list of services to be configured on destnComputer through a list (of objects of class Service) 
    destnComputer.services. See fetchClientDetails.py file for attributes of class Service
    '''
    logFile.write('\n------------Configuring services started------------\n')
    try:
        for service in destnComputer.services:
            
            '''
            Here is a catch, if we try configuring all the services through a single ssh
            connection, we may not be able to configure few services. Hence for every service,
            we need to 1. connect to destnComputer, 2. start/stop it, 3. and then disconnect from destnComputer
            '''
            srcComputer.connect(destnComputer, logFile)
            servicename = service.name  #name of the service
            action = service.action     #whether to start or stop the service
            print(servicename, ' to be ', action)
            logFile.write('\n'+servicename+' to be '+action)
            
            if action == 'start':
                #before we either start or stop the service, we try figuring out the
                #current status of that service on the destnComputer
                
                if destnComputer.serviceStatus(servicename) == 0: 
                    '''
                    means the 'servicename' service is currently stopped on the destnComputer
                    hence start 'servicename' service
                    Also recall it is the srcComputer that has the channel open to the destnComputer, hence it is 
                    srcComputer.channel.exec_command(...) instead of destnComputer.channel.exec_command(...)
                    '''
                    i, o, e = srcComputer.channel.exec_command('net start '+servicename+' /yes')
                    
                    error = e.readlines()
                    #if the error file is not empty, it means some error has been returned by exec_command function
                    if len(error)>0:
                        print '\nError configuring service '+servicename
                        logFile.write('\nError configuring service '+servicename)
                        for line in error:
                            print(line)
                            logFile.write(line) 
                    else:
                        print(servicename, ' successfully started')
                        logFile.write('\n'+servicename+' successfully started')
                    
                else:
                    print(servicename,' is already running')
                    logFile.write('\n'+servicename+' is already running')
            
            elif action == 'stop':
                if destnComputer.serviceStatus(servicename) == 1:
                    #servicename was running on destnComputer, hence stop it
                    i, o, e = srcComputer.channel.exec_command('net stop '+servicename+' /yes')
                    error = e.readlines()
                    if len(error)>0:
                        print '\nError configuring service '+servicename
                        logFile.write('\nError configuring service '+servicename)
                        for line in error:
                            print(line)
                            logFile.write(line) 
                    else:
                        print(servicename, ' successfully stopped')
                        logFile.write('\n'+servicename+' successfully stopped')                     

                else:
                    print(servicename, ' was already stopped')
                    logFile.write('\n'+servicename+' was already stopped')
            
            srcComputer.disconnect(destnComputer, logFile)
            #recall, 1. connect, 2. configure, 3. disconnect, repeating this 
            #for all services in the list destnComputer.service
            
        logFile.write('\n------------Configuring sevices completed------------\n')
            
    except Exception as e:
        print('Error while configuring services')
        logFile.write('\nError while configuring services, from function startStopServices in functionalities.py file\n'+str(e))



def preCopy(srcComputer, destnComputer, logFile):
    '''
    preCopy(...) cretes a directory on destnComputer, copies all the msis into this directory
    and returns the full path of this directory which will be used by triggerMSIs(...)
    '''
    try:
        print('copying files for installation started')
        logFile.write('\nCopying files for installation started')
        srcComputer.connect(destnComputer, logFile)
        
        #open an sftp channel to copy all the msis
        sftp = srcComputer.channel.open_sftp()
        
        #devise a random name, trying as far as possible to avoid name clashes with the
        #directories already present on destnComputer
        temp = ''.join(random.choice(string.ascii_uppercase) for _ in range(16))

        #create this directory on destnComputer
        sftp.mkdir('C:\\Users\\Public\\'+temp)
        logFile.write('\nMaking a temporary directory C:\\Users\\Public\\'+temp)
        
        #copy all the msis into this directory, path contains the path of msi on the srcComputer
        #'C:\\Users\\Public\\'+temp+'\\'+str(msi.path[msi.path.rfind('\\')+1:]) is the destined path
        #of the msi on destnComputer
        for msi in destnComputer.msis:
            path = msi.path
            sftp.put(path, r'C:\\Users\\Public\\'+temp+'\\'+str(msi.path[msi.path.rfind('\\')+1:]))
            logFile.write('\nCopied the msi '+path)
        
        '''
        NOTE: For triggering these copied msis on destnComputer, we have a workaround. We write a python script
        here, all which does is execute subprocess.call('msiexec /i <path_to_msi>') for each of the msi file.
        Next through the exec_command operation, we execute this python script on destnComputer.
        We could have done this using a direct msiexec call from the exec_command function 
        using srcComputer.channel.exec_commad('msiexec /i <path_to_msi>) but a direct call to msiexec from
        the remote system wasn't working, because of which we had to use the python script workaround.
        '''
        
        logFile.write('\nWriting the python script for installation')
        
        #open a python script in write mode
        f = open(r'C:\Users\39232\Desktop\Project Files\installingCode.py','w')
        #write the codes into the python file
        f.write('import subprocess\n')
        for msi in destnComputer.msis:
            f.write('\na = subprocess.call(r\'msiexec /i '+r'C:\\Users\\Public\\'+temp+'\\'+str(msi.path[msi.path.rfind('\\')+1:])+'\')\n')
            #f.write('time.sleep(2)\n')
            f.write('if a!=0:\n\tprint\''+str(msi.path[msi.path.rfind('\\')+1:])+' failed to execute on the remote system\'\n')
            f.write('else:\n\tprint\''+str(msi.path[msi.path.rfind('\\')+1:])+' successfully installed on the remote system\'\n')
        f.close()
        logFile.write('\nCompleted the python script for installation')
        '''
        the file installingScript.py has,
        import subprocess
        a = subprocess.call('msiexec /i C:\\Users\\Public\\<temporaryDirectoryName>\\<msiFile>
        if a!=0:
            print 'msi failed to execute on the remote system'
        else:
            print 'msi successfully installed on the remote system
        '''
        #next, copy this installingCode.py to destnComputer
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
    '''
    triggerMSIs(...) executes the copied python script installingCode.py on destnComputer
    resulting in installation of all the mentioned msis in the installingCode.py file
    triggerMSIs(...) takes 'path' as input which is the full path of installingCode.py on destnComputer
    '''
    try:
        pathnew = path.replace('\\','/')
        '''
        path contained backslashes, which need to be converted to forward 
        slashes to be able to be interpreted in exec_command
        exec_command gives error with backslashes
        '''
        srcComputer.connect(destnComputer, logFile)
        print('installations started')
        logFile.write('\ninstallations started on client')
        
        '''
        NOTE: Here lies one requirement for this project. The client should have python 2.7 version installed on
        it and the installed directory should be C:\\Python27 only. We can achieve a little flexibility though by
        taking the installed directory of python on destnComputer in command line argument, but still the version is
        restricted to 2.7 only.
        '''
        stdin, stdout, stderr = srcComputer.channel.exec_command(r'C:/Python27/python '+pathnew+'/installingCode.py')
        output = stdout.readlines()
        error = stderr.readlines()
        
        #if the error file is not empty, it means some error has occurred
        if len(error) > 0:
            print('Error in excuting msis : ',error)
            logFile.write('\nError in excuting msis : '+error)
        
        #log all the output returned by the exec_command function
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
    '''
    removeCopiedFiles(...) deletes all the msi files preCopy(...) function had copied to destnComputer.
    It also removes the temporary directory which preCopy(...) function had created on destnComputer.
    '''
    try:
        print('removing the copied msis')
        logFile.write('\nremoving the copied msi files')
        
        srcComputer.connect(destnComputer, logFile)
        sftp = srcComputer.channel.open_sftp()
        
        #list all the files in the temporary directory whose full path is 'path'
        filesInDestnSystem = sftp.listdir(path)
        
        #now remove all of them
        for files in filesInDestnSystem:
            sftp.remove(path+'\\'+files)
            logFile.write('\nremoved '+path+'\\'+files)
            
        #next remove the temporary directory as well
        sftp.rmdir(path)
        logFile.write('\nRemoving the temporary directory '+path)
        
        sftp.close()
        srcComputer.disconnect(destnComputer, logFile)
        print('removing successful')
        logFile.write('\nSuccessfully removed the temporary directory')
               
    except Exception as e:
        print('removing copied files failed')
        logFile.write('\nFrom function removeCopiedFiles in functionalities.py file, Error : '+str(e))
        


def remoteInstallation(srcComputer, destnComputer, logFile):
    '''
    remoteInstallation(...) does a installation of all the msi files mentioned in the list destnComputer.msis
    destnComputer.msis is a list of objects of Class MSI, see fetchClientDetails.py file for the attributes of class MSI
    '''
    logFile.write('\n------------Installations Started------------\n')
    
    #copy all the msis (to be installed on destnComputer) to the destnComputer
    #precopy return the full path of the directory on destnComputer where the msis are copied
    path = preCopy(srcComputer, destnComputer, logFile)
    
    #execute the copied msis one at a time on destnComputer
    triggerMSIs(srcComputer, destnComputer, path, logFile)
    
    #remove the copied msis from destnComputer
    #removeCopiedFiles(srcComputer, destnComputer, path, logFile)
    
    logFile.write('\n------------Installations Ended------------\n')