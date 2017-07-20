import sys
import json

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
def parsing(obj, clientIndex, configFile):

    '''
#debugging line starts
if __name__ == '__main__':
    configFile = r'C:\Users\39232\Desktop\Project Files\configFileFinal.json'
    obj = Dummy()
    clientIndex = 0
    #debugging lines end
    '''
    
    
    print('parsing started\n')
    with open(configFile) as data_file:
        data = json.load(data_file)
        
    thisSystem = data[clientIndex]
    thisSystemDetails = thisSystem['details']
    
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

    
    listofmsis = thisSystem['msi']
    for msi in listofmsis:
            m = MSI()
            m.path = str(msi['path'])
            obj.msis.append(m)
    for msi in obj.msis:
        print msi.path[msi.path.rfind('\\')+1:]
    
    print('Parsing Ended\n')
    
    #debugging line
    #print obj, thisSystemDetails['ip'], thisSystemDetails['username'], thisSystemDetails['password']
    
    #original line
    return obj, thisSystemDetails['ip'], thisSystemDetails['username'], thisSystemDetails['password']
          
    