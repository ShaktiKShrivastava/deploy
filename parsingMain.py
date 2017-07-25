import json
#need to import main also in order to use the global variable logFile

def parsingFromDisk(configFile, logFile):
    #configFile = r"C:\Users\39232\Desktop\Project Files\configFileFinal.json"
    #global logFile
    try:
        logFile.write('\nparsing the config file started')
        print('\nparsing the config file started')
        with open(configFile) as data_file:
            data = json.load(data_file)
        
        mapping = {}   
        for clientIP in data:
            thisSystem = data[clientIP]
            
            mapping[clientIP] = {}
            mapping[clientIP]['username'] = thisSystem['username']
            mapping[clientIP]['password'] = thisSystem['password']
            
            listofPackages = thisSystem['packages']
            mapping[clientIP]['packages'] = []
            for pkg in listofPackages:
                p = {}
                p['source'] = str(pkg['source'])
                p['destn'] = str(pkg['destn'])
                p['name'] = str(pkg['name'])
                mapping[clientIP]['packages'].append(p)
        
            listofServices = thisSystem['services']
            mapping[clientIP]['services'] = []
            for service in listofServices:
                    s = {}
                    s['name'] = str(service['name'])
                    s['action'] = str(service['action'])
                    mapping[clientIP]['services'].append(s)
                
            listofmsis = thisSystem['msi']
            mapping[clientIP]['msis'] = []
            for msi in listofmsis:
                m = {}
                m['path'] = str(msi['path'])
                mapping[clientIP]['msis'].append(m)
        '''
        for el in mapping:
            print mapping[el]['username']
            print mapping[el]['password']
            for p in mapping[el]['packages']:
                print p['source'], p['destn'], p['name']
            for m in mapping[el]['msis']:
                print m['path']
            for s in mapping[el]['services']:
                print s['name'], s['action']
    ''' 
        logFile.write('\nparsing the config file ended')
        print('parsing the config file ended\n')
        
        return mapping
    except Exception as e:
        logFile.write('\nError while processing the config file, error is\n'+str(e))
        print('Error while processing the config file, error is\n'+str(e))
        logFile.write('\nProgram exited')
        