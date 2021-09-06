@echo off
pip install -r requirements.txt
pyinstaller main.py --add-data logo.png;. --noconsole -i icon.ico
if exist %UserProfile%\dpsht rmdir /S %UserProfile%\dpsht
xcopy /s .\dist\main\ %UserProfile%\dpsht
set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = "%appdata%\Microsoft\Windows\Start Menu\DPSHT.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "%UserProfile%\dpsht\main.exe" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%

cscript /nologo %SCRIPT%
del %SCRIPT%