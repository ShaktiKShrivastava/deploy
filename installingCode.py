import subprocess

try:
	subprocess.call('msiexec /i abba')
except:
	print 'program abba failed to execute on the remote system'
try:
	subprocess.call('msiexec /i jabba')
except:
	print 'program jabba failed to execute on the remote system'