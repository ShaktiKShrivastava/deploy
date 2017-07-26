import sys
    
class Package:
    '''
    objects of class Package will hold information about
    the packages to be deployed on the client systems
    '''
    def __init__(self):
        self.src = None     #path of the package on the server
        self.destn = None   #destined path of the package on the client system
        self.name = None    #a name for the package

class Service:
    '''
    objects of class Service will hold information about
    the services to be configured on the client systems
    '''
    def __init__(self):
        self.name = None    #name of the service
        self.action = None  #whether to start or stop the service

class MSI:
    '''
    objects of class MSI will hold information about
    the msis to be installed on the client systems
    '''
    def __init__(self):
        self.path = None    #path of the msi on the server system

def fetchClientDetails(obj, configFileData, clientIP, logFile):
    '''
    This function reads the configFileData which is the dictionary returned by
    parsingFromDisk(...) function, and constructs the lists <Client_object>.packages,
    <Client_object>.services and <Client_object>.msis respectively.
    <Client_object>.packages is a list of objects of class Package, containing information
    about all the package to be deployed on the system refered to be <Client_object>
    Similar explanation holds for <Client_object>.services and <Client_object>.msis
    fetchClientDetails(...) returns, in addition to the Client object, the IP address of
    the username and password of the refered client
    '''
    
    try:
        thisSystem = configFileData[clientIP]
        #recall the structure of mapping from parsingMain.py. The data in configFileData is hence
        #keyed by the IP addresses of the different client system
        
    except:
        logFile.write('\n'+clientIP+' not found in clients, program exiting')
        print (clientIP,' not found in clients')
        #in case the clientIP passed to fetchClientDetails(...) doesn't exist in the configFileData
        sys.exit()
        
    try:  
        logFile.write('\nFetching client '+clientIP+' details') 
        
        listofPackages = thisSystem['packages']
        for pkg in listofPackages:
                #create an object of class Package for each of the packages for 
                #the client with IP = clientIP
                p = Package()
                p.src = str(pkg['source'])
                p.destn = str(pkg['destn'])
                p.name = str(pkg['name'])
                #append this object to the list obj.packages
                obj.packages.append(p)
        
        #similarly, create lists obj.services and obj.msis
        listofServices = thisSystem['services']
        for service in listofServices:
                s = Service()
                s.name = str(service['name'])
                s.action = str(service['action'])
                obj.services.append(s)
    
        listofmsis = thisSystem['msis']
        for msi in listofmsis:
                m = MSI()
                m.path = str(msi['path'])
                obj.msis.append(m)
        
        logFile.write('\nFollowing packages will be copied to'+clientIP+'\n')
        for pkg in obj.packages:
            print pkg.src, pkg.destn, pkg.name
            logFile.write('\n'+pkg.src+' '+pkg.destn+' '+pkg.name)
        
        logFile.write('\nFollowing services will be configured on '+clientIP+'\n')
        for s in obj.services:
            print s.name, s.action
            logFile.write('\n'+s.name+' '+s.action)
        
        logFile.write('\nFollowing MSIs will be installed on '+clientIP+'\n')
        for msi in obj.msis:
            print msi.path[msi.path.rfind('\\')+1:]
            logFile.write('\n'+msi.path[msi.path.rfind('\\')+1:])
        
        print('Client details fetched\n')
        logFile.write('\nClient details fetched')
        
        return obj, thisSystem['username'], thisSystem['password']
    
    except Exception as e:
        print('Error while fetching client details.\n',str(e))    
        logFile.write('\nError while fetching client details.\n'+str(e))
    