import os
import os.path
import sys
import shutil
import zipfile
import tempfile


def remove_from_zip(zipfname, *filenames):
    tempdir = tempfile.mkdtemp()
    try:
        tempname = os.path.join(tempdir, 'new.zip')
        with zipfile.ZipFile(zipfname, 'r') as zipread:
            with zipfile.ZipFile(tempname, 'w') as zipwrite:
                for item in zipread.infolist():
                    if item.filename not in filenames:
                        data = zipread.read(item.filename)
                        zipwrite.writestr(item, data)
        shutil.move(tempname, zipfname)
    finally:
        shutil.rmtree(tempdir)


def APKmodify(apkFile):	
	
	#Edit the manifest to give access to the code added
	os.system('java -jar apktool.jar d '+apkFile+'.apk -o '+apkFile+'-dir-apktool')
	print '\n\n=> Time to edit the AndroidManifest.xml in '+apkFile+'-dir-apktool.'
	print '==>Press ENTER to continue.'
	raw_input()
	
	#Modify and add code to the APK  
	os.system('d2j-dex2jar -f -o '+apkFile+'-dex2jar.jar '+apkFile+'.apk')
	os.system('d2j-jar2jasmin -f -o '+apkFile+'-dir '+apkFile+'-dex2jar.jar')
	print '\n\n=> Time to edit the code in '+apkFile+'-dir.'
	print '==>Press ENTER to continue.'
	raw_input()

	#Reassembling of the code
	os.system('java -jar apktool.jar b '+apkFile+'-dir-apktool -o '+apkFile+'-manifest.apk')
	os.system('d2j-jasmin2jar -f  -o '+apkFile+'-edited.jar  '+apkFile+'-dir')
	os.system('d2j-jar2dex  -f -o classes.dex '+apkFile+'-edited.jar')
	shutil.copyfile(apkFile+'.apk', apkFile+'-edited.apk')
	
	#Forge the APK with the modifications
	zip_out = zipfile.ZipFile(apkFile+'-manifest.apk')
	zip_out.extract('AndroidManifest.xml','.')
	zip_out.close()
	
	files_to_remove = ['classes.dex', 'AndroidManifest.xml']
	remove_from_zip(apkFile+'-edited.apk', *files_to_remove)	
	zip_in = zipfile.ZipFile(apkFile+'-edited.apk', "a")
	zip_in.write('classes.dex')
	zip_in.write('AndroidManifest.xml')
	zip_in.close()
	
	#Sign the APK forged
	os.system('d2j-apk-sign -f -o '+apkFile+'-sign.apk '+apkFile+'-edited.apk')
	print '\n\n=> The modified file '+apkFile+'-sign.apk is ready to be installed'
	
	#Remove all the temporal files
	if(os.path.exists('classes.dex')):
		try:
			os.remove('classes.dex')
		except:
			print 'Could not remove the file classes.dex'
		
	if(os.path.exists('AndroidManifest.xml')):
		try:
			os.remove('AndroidManifest.xml')
		except:
			print 'Could not remove the file AndroidManifest.xml'
		
	if(os.path.exists(apkFile+'-dir-apktool')):
		try:
			shutil.rmtree(apkFile+'-dir-apktool')
		except:
			print 'Could not remove the dir '+apkFile+'-dir-apktool'
		
	if(os.path.exists(apkFile+'-dir')):
		try:
			shutil.rmtree(apkFile+'-dir')
		except:
			print 'Could not remove the dir '+apkFile+'-dir'
		
	if(os.path.exists(apkFile+'-dex2jar.jar')):
		try:
			os.remove(apkFile+'-dex2jar.jar')
		except:
			print 'Could not remove the file '+apkFile+'-dex2jar.jar'
		
	if(os.path.exists(apkFile+'-edited.jar')):
		try:
			os.remove(apkFile+'-edited.jar')
		except:
			print 'Could not remove the file '+apkFile+'-edited.jar'
		
	if(os.path.exists(apkFile+'-manifest.apk')):
		try:
			os.remove(apkFile+'-manifest.apk')
		except:
			print 'Could not remove the file '+apkFile+'-manifest.apk'
		
	if(os.path.exists(apkFile+'-edited.apk')):
		try:
			os.remove(apkFile+'-edited.apk')
		except:
			print 'Could not remove the file '+apkFile+'-edited.apk'
	


if __name__ == '__main__':
	
	if(len(sys.argv) == 2 and sys.argv[1].endswith('.apk') and os.path.isfile(sys.argv[1])):
		APKmodify(sys.argv[1][:-4])
		
	else:
		print '\nInvalid parameters or the file it\'s not accessible.\n\nUsage: ./modify.py file.apk\n'
		sys.exit(0)
