import json

def parsingFromDisk(configFile, logFile):
    '''
    parsingFromDisk(...) reads the configuration file 'configFile' and parses
    the data from it to create a dictionary structure. In this way, instead of
    requiring IO operation evrytime we need some data from the configuration file,
    we can directly read it from the dictionary which is there in memory
    parsingFromDisk(...) returns the parsed data in the form of a dictionary.
    '''
    try:
        logFile.write('\nparsing the config file started')
        print('\nparsing the config file started')
        
        #we used python's json module to parse the configuration file. Note that
        #configFile is a json file format
        with open(configFile) as data_file:
            data = json.load(data_file)
        
        #mapping is the dictionary that will hold the data extracted from configFile
        #the structure of mapping is given at the end of this function
        mapping = {}   
        
        #configFile has data keyed by IP address of the client systems
        for clientIP in data:
            thisSystem = data[clientIP]
            
            #initialise an empty dictionary with key as clientIP
            mapping[clientIP] = {}
            mapping[clientIP]['username'] = thisSystem['username']
            mapping[clientIP]['password'] = thisSystem['password']
            #thus each mapping[clientIP] is itself a dictionary, with keys username, 
            #password and other fields we'll see now
            
            listofPackages = thisSystem['packages']
            #mapping[clientIP]['packages'] is a list of dictionaries, each having
            #source, destination, and name of the packages for the client clientIP
            mapping[clientIP]['packages'] = []
            for pkg in listofPackages:
                p = {}
                p['source'] = str(pkg['source'])
                p['destn'] = str(pkg['destn'])
                p['name'] = str(pkg['name'])
                mapping[clientIP]['packages'].append(p)
            
            listofServices = thisSystem['services']
            #mapping[clientIP]['services'] is a list of dictionaries, each having
            #name and action of the services to be configured for the client clientIP
            mapping[clientIP]['services'] = []
            for service in listofServices:
                    s = {}
                    s['name'] = str(service['name'])
                    s['action'] = str(service['action'])
                    mapping[clientIP]['services'].append(s)
                
            listofmsis = thisSystem['msi']
            #mapping[clientIP]['msis'] is a list of dictionaries, each having
            #local path of the msi on the server system
            mapping[clientIP]['msis'] = []
            for msi in listofmsis:
                m = {}
                m['path'] = str(msi['path'])
                mapping[clientIP]['msis'].append(m)
        
        logFile.write('\nparsing the config file ended')
        print('parsing the config file ended\n')
        
        return mapping
        '''
        Thus we see that mapping is a nested dictionary, the structure of mapping conforms to,
        mapping = {
                    'client_1_IP':
                        {
                        'username':<username>,
                        'password':<password>,
                        'packages':
                            [
                                {
                                'source':<path_of_source_on_local_machine>
                                'destn':<path_of_destn_on_remote_machine>
                                'name':<some_name_of_the_package>
                                },
                                {
                                'source':<path_of_source_on_local_machine>
                                'destn':<path_of_destn_on_remote_machine>
                                'name':<some_name_of_the_package>
                                },...
                            ],
                        'services':
                            [
                                {
                                'name':<name_of_service_to_be_configured>
                                'action':<start/stop>
                                },
                                {
                                'name':<name_of_service_to_be_configured>
                                'action':<start/stop>
                                },...
                            ],
                        'msis':
                            [
                                {
                                'path':<path_of_msi_on_server_system>
                                },
                                {
                                'path':<path_of_msi_on_server_system>
                                },...
                            ]
                        },
                    client_2_IP:
                        {
                        ...
                        },
                    ...                        
                 }
        Thus the structure of mapping is same as the structure of the configguration file which is in json format.
        '''
        
    except Exception as e:
        logFile.write('\nError while processing the config file, error is\n'+str(e))
        print('Error while processing the config file, error is\n'+str(e))
        logFile.write('\nProgram exited')
        