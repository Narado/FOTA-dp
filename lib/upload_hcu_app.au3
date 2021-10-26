

Local $vVariavle
;$vPATH = "C:\Users\lei.gao\AppData\Local\Programs\Python\Python39\Lib\site-packages\MyLibrary\FOTA\dp\HCU\HCUapp.s19"
$vPATH = IniReadSection("..\conf\Fota.ini","hcuconf")

;ContorlFocus("title","text",controlID) Edit1=Edit instance 1
ControlFocus("打开","","Edit1")

;wait 10 seconds for the Upload window to appear
Winwait("[CLASS:#32770]","",10)

;Set the File name text on the Edit field
ControlSetText("打开","","Edit1",$vPATH[2][1])

Sleep(2000)

;Click on the Open buttons
ControlClick("打开","","Button1");
