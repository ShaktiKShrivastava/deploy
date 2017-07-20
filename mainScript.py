import paramiko, sys
from classes import *

you = Server('192.168.56.1')
him = Client(sys.argv[2])