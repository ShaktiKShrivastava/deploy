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
def fetchClientDetails(obj, configFileData, clientIP):

    '''    
#debugging line starts
if __name__ == '__main__':
    configFile = r'C:\Users\39232\Desktop\Project Files\configFileFinal.json'
    obj = Dummy()
    configFileData = parsingFromDisk(r"C:\Users\39232\Desktop\Project Files\configFileFinal.json")
    clientIP = '1.1.1.1'
    #debugging lines end
    '''
   
    thisSystem = configFileData[clientIP]
    
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
    
    
    for pkg in obj.packages:
        print pkg.src, pkg.destn, pkg.name
    for s in obj.services:
        print s.name, s.action
    for msi in obj.msis:
        print msi.path[msi.path.rfind('\\')+1:]
    
    print('Client details fetched\n')
    
    #debugging line
    #print obj, clientIP, thisSystem['username'], thisSystem['password']
    
    #original line
    return obj, thisSystem['username'], thisSystem['password']
          
    