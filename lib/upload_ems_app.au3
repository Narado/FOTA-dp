

Local $vVariavle
;$vPATH = "C:\04_AFC_package\AFC-100-AH-CN_V4.1.0_20210805_Filtered\EMS0A001R410_20210805\EMSAH32S0409R21_0728.s19"
$vPATH = IniReadSection("..\conf\Fota.ini","emsconf")

;ContorlFocus("title","text",controlID) Edit1=Edit instance 1
ControlFocus("打开","","Edit1")

;wait 10 seconds for the Upload window to appear
Winwait("[CLASS:#32770]","",10)

;Set the File name text on the Edit field
ControlSetText("打开","","Edit1",$vPATH[2][1])

Sleep(2000)

;Click on the Open buttons
ControlClick("打开","","Button1");
