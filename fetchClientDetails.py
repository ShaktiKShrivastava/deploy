import sys
'''
#debugging lines start
class Dummy:
    def __init__(self):
        self.packages = []
        self.services = []
        self.msis = []
#debugging line ends
'''
    
class Package:
    def __init__(self):
        self.src = None
        self.destn = None
        self.name = None

class Service:
    def __init__(self):
        self.name = None
        self.action = None

class MSI:
    def __init__(self):
        self.path = None

#original line
def fetchClientDetails(obj, configFileData, clientIP, logFile):

    '''    
#debugging line starts
if __name__ == '__main__':
    configFile = r'C:\Users\39232\Desktop\Project Files\configFileFinal.json'
    obj = Dummy()
    configFileData = parsingFromDisk(r"C:\Users\39232\Desktop\Project Files\configFileFinal.json")
    clientIP = '1.1.1.1'
    #debugging lines end
    '''
    
    try:
        thisSystem = configFileData[clientIP]
    except:
        logFile.write('\n'+clientIP+' not found in clients, program exiting')
        print (clientIP,' not found in clients')
        sys.exit()
        
    try:  
        logFile.write('\nFetching client '+clientIP+' details') 
        
        listofPackages = thisSystem['packages']
        for pkg in listofPackages:
                p = Package()
                p.src = str(pkg['source'])
                p.destn = str(pkg['destn'])
                p.name = str(pkg['name'])
                obj.packages.append(p)
        
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
        
        
        #debugging line
        #print obj, clientIP, thisSystem['username'], thisSystem['password']
        
        #original line
        return obj, thisSystem['username'], thisSystem['password']
    except Exception as e:
        print('Error while fetching client details.\n',str(e))    
        logFile.write('\nError while fetching client details.\n'+str(e))
    