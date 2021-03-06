; Script generated by the Inno Script Studio Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{AE2FFB4F-8579-4037-89CD-E1ADD6373A05}
;SignTool=signtool $f
AppName=Emood
AppVersion=0.25
;AppVerName=Emood Demo 0.2
AppPublisher=Custom Group
AppPublisherURL=https://emood.com.ar/
AppSupportURL=https://emood.com.ar/
AppUpdatesURL=https://emood.com.ar/
DefaultDirName={pf}\Emood
DefaultGroupName=Emood
OutputBaseFilename=setup
SetupIconFile=C:\Users\frank\Documents\emood\emood\build\EmoodWin\src\logo.ico
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Dirs]
Name: "{app}"; 
Name: "{app}\"; Permissions: everyone-full
Name: "{app}\src\"; Permissions: everyone-full

[Files]
Source: "C:\Users\frank\Documents\emood\emood\build\EmoodWin\emood.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\frank\Documents\emood\emood\build\EmoodWin\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\Emood Demo"; Filename: "{app}\start.exe"
Name: "{group}\{cm:UninstallProgram,Emood Demo}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Emood"; Filename: "{app}\emood.exe"; Tasks: desktopicon
Name: "{commonstartup}\Emood"; Filename: "{app}\emood.exe"

[Run]
Filename: "{app}\emood.exe"; Description: "{cm:LaunchProgram,Emood}"; Flags: nowait postinstall skipifsilent

