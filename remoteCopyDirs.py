'''
to resolve symlinks still
the symlink files are copied with their content but they no longer remain symlinks,
rather they become normal files

'''
import paramiko, os

ip = '192.168.56.101'
username = 'IEUser'
password = 'Passw0rd!'

client1 = paramiko.SSHClient()

client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())


client1.connect('192.168.56.102',22,'IEUser','Passw0rd!')

sftp = client1.open_sftp()
src = 'C:\\Users\\39232\\Desktop\\1'
destn = 'C:\\Users\\Public\\Exp'
print src, destn

try:
    
    for root, dirs, files in os.walk(src, topdown=True):
        
        print root
        print 'this is the root',root
        
        print 'files are'
        for name in files:
            print name
            print 'from source ',os.path.join(root,name)
            print 'to destn ',destn+'\\'+root.replace(src,'')+'\\'+name
            sftp.put(os.path.join(root,name), destn+'\\'+root.replace(src,'')+'\\'+name)
            
        
        print 'dirs are'
        for name in dirs:
            print name
            sftp.mkdir(destn+'\\'+root.replace(src,'')+'\\'+name, 0777)
            
        print 'changing loop\n\n'

except WindowsError:
    print '\n\nError while copying, the values retrived at error point were'
    print 'destn : ',destn,' root : ',root, 'name : ',name
except IOError:
    print '\n\nError while copying, the values retrived at error point were'
    print 'destn : ',destn,' root : ',root, 'name : ',name

client1.close()