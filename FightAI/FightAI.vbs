Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
cmdPath = Chr(34) & fso.BuildPath(scriptDir, "FightAI.cmd") & Chr(34)

shell.Run cmdPath, 0, False
