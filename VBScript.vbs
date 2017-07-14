Dim strInstaller 'The command to install the software package
Dim strComputer 'The Computer
Dim objWMIService 
Dim strProcess 'The process to terminate before running the command
Dim objProcess
Dim objFSO
Dim strFilePath 'The filename and path to the installer package
Dim strDestination 'the filename and path on the destination computer for the package
Dim colProcess 
Dim intProcessID 'The number assigned to the process that is created

'Set the variables

StrInput = InputBox("Enter IP address of the system")
strComputer = StrInput
strInstaller = "msiexec.exe /i C:\Users\39232\Desktop\shakti_kumar.msi"
strFilePath = "c:\Users\39232\Desktop\shakti_kumar.msi"
strDestination = "C:\Users\39232\Desktop\shakti_kumar2.msi"

'Display the variables when it runs
WScript.Echo "Target Computer: " & strComputer
WScript.Echo "Command: " & strInstaller
WScript.Echo "Package: " & strDestination

'Copy the installer package to the target PC
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objFileCopy = objFSO.GetFile(strFilePath)
objFileCopy.Copy(strDestination)

'Start the installer
Set objWMIService = GetObject("winmgmts:" & "{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2:Win32_Process")
errReturn = objWMIService.Create(strInstaller, Null, Null, intProcessID)

If errReturn = 0 Then
 WScript.Echo "Installer was started with a process ID of " & intProcessID
  Else
 Wscript.Echo strProcess & " could not be started due to error " & errReturn
End If

WScript.Quit
