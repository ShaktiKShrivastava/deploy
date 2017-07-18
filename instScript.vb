Dim oShell, ofso, ScriptDIr, ErrorCode 
 
Set oShell = CreateObject("WScript.Shell")
Set ofso = CreateObject("Scripting.FileSystemObject")
ScriptDIr = oFSO.GetParentFolderName(Wscript.ScriptFullName)
 
ErrorCode = oShell.Run("MSIEXEC /I " & Chr(34) & ScriptDIr & "\sample.msi" & Chr(34) & " /L*V C:\INSTA_LOGS\SETUP_Install.LOG /QB!-", 0, True) 
WScript.Quit(ErrorCode)
 
Set oShell = Nothing
Set ofso = Nothing
Set oReg = Nothing