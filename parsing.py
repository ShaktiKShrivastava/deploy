import json

def parsing():
        
    with open(r'C:\Users\39232\Desktop\Project Files\configFileFinal.json') as data_file:
        data = json.load(data_file)
        
    noOfSystems = len(data)
    
    for i in range(1,noOfSystems+1):
        thisSystem = data['System'+str(i)]
        
        thisSystemDetails = thisSystem['details']
        thisSystemPackages = thisSystem['packages']
        thisSystemServices = thisSystem['services']
        thisSystemCommands = thisSystem['commands']
        
        