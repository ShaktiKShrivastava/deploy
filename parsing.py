import sys, json, time

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

def parsing(obj, clientIndex, configFile):
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
    
    '''        
    print(obj,thisSystemDetails['ip'],thisSystemDetails['username'],thisSystemDetails['password'])
    
    
    print('from parsing function\n\n')
    for el in obj.packages:
        print(el.src, el.destn, el.name)
        
    for el in obj.services:
            print(el.name, el.action)
    
    for el in obj.msis:
        print(el.path)
    '''
    print('Parsing Ended\n')
    
    
    return obj,thisSystemDetails['ip'],thisSystemDetails['username'],thisSystemDetails['password']
          
    