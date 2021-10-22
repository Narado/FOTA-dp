

Local $vVariavle
$vPATH = "C:\Users\lei.gao\AppData\Local\Programs\Python\Python39\Lib\site-packages\MyLibrary\FOTA\dp\EMS\ems_udsflash_v2.0.ini"


;ContorlFocus("title","text",controlID) Edit1=Edit instance 1
ControlFocus("打开","","Edit1")

;wait 10 seconds for the Upload window to appear
Winwait("[CLASS:#32770]","",10)

;Set the File name text on the Edit field
ControlSetText("打开","","Edit1",$vPATH)

Sleep(2000)

;Click on the Open buttons
ControlClick("打开","","Button1");
