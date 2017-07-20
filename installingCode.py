import subprocess, time

a = subprocess.call(r'msiexec /i C:\Users\Public\Exp\shakti_kumar.msi')
time.sleep(2)
if a!=0:
	print'C:\Users\Public\Exp\shakti_kumar.msi failed to execute on the remote system'
else:
	print'C:\Users\Public\Exp\shakti_kumar.msi successfully installed on the remote system'

a = subprocess.call(r'msiexec /i C:\Users\Public\Exp\cab1.cab')
time.sleep(2)
if a!=0:
	print'C:\Users\Public\Exp\cab1.cab failed to execute on the remote system'
else:
	print'C:\Users\Public\Exp\cab1.cab successfully installed on the remote system'
