#! /usr/bin/python

import os
import os.path
import sys


def modifyProcess(apkFile):
	os.system("apktool.jar d "+apkFile+".apk "+apkFile+"-dir-apktool")
	print "\r\n==> Time to edit the AndroidManifest.xml in "+apkFile+"-dir-apktool. Press ENTER to continue."
	raw_input()
	os.system("d2j-dex2jar -f -o "+apkFile+"-dex2jar.jar "+apkFile+".apk")
	os.system("d2j-jar2jasmin -f -o "+apkFile+"-dir "+apkFile+"-dex2jar.jar")
	print "\r\n==> Time to edit the code in "+apkFile+"-dir. Press ENTER to continue."
	raw_input()
	os.system("apktool.jar b "+apkFile+"-dir-apktool "+apkFile+"-manifest.apk")
	os.system("d2j-jasmin2jar -f  -o "+apkFile+"-edited.jar  "+apkFile+"-dir")
	os.system("rm classes.dex")
	os.system("d2j-jar2dex  -f -o classes.dex "+apkFile+"-edited.jar")
	os.system("cp "+apkFile+".apk "+apkFile+"-edited.apk")
	print "\r\n==> The modified classes.dex and AndroidManifest.xml are stored in "+apkFile+"-manifest.apk. Unzip this APK and add those files to "+apkFile+"-edited.apk. Press ENTER to continue."
	raw_input()
	os.system("d2j-apk-sign -f -o "+apkFile+"-sign.apk "+apkFile+"-edited.apk")
	print "\r\n==> The modified file "+apkFile+"-sign.apk its ready to be installed"

if __name__ == "__main__":
	if(len(sys.argv) == 2 and sys.argv[1].endswith(".apk") and os.path.isfile(sys.argv[1])):
		modifyProcess(sys.argv[1][:-4])
	else:
		print '\nInvalid parameters or the file it\'s not accessible.\n\nUsage: ./modify.py file.apk\n'
		sys.exit(0)