#! /usr/bin/python

import os
import sys
import zipfile
import subprocess
import glob
import re


def printBanner(file, msg):
	
	file.write('\n\n####################################\n')
	file.write('\tResults for ' + msg + '\n')
	file.write('####################################\n\n')
	
	

def analyze(input_file, output_directory, report_file):
	
	regex_dict = {
				'URLs': 'https?:\/\/?[\da-z\.-]+\.[a-z\.]{2,6}[\/\w \.-]*\/?', 
				'email': '[a-zA-Z1-9]+@[a-zA-Z1-9]+\.[a-zA-Z]{2,4}',
				'IPs': '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
				'Whatsapp' : 'whatsapp',
				'Facebook' : 'facebook',
				'Dropbox' : 'dropbox',
				'Gmail' : 'gmail',
				}
	
	#Disassemble the APK and resource extraction
	os.system('apktool.jar d ' + input_file + ' ' + output_directory)
	
	#Generate JAR for jd-gui analysis
	os.system('d2j-dex2jar ' + input_file + ' -f -o ' + output_directory + input_file + '.jar')
	
	#Extraction of the cert
	zip = zipfile.ZipFile(input_file)
	for name in zip.namelist():
		if(name.lower().endswith('rsa')):
			zip.extract(name, output_directory)
	
	#Open report file
	report = open(report_file, 'w')
	
	#Write cert info
	printBanner(report, "Certificate")
	command = 'keytool -printcert -file ' + output_directory + 'META-INF/*.RSA'
	proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=False)
	(out, err) = proc.communicate()
	report.write(out)
	
	#Prepare the result data structure
	result = dict()
	for key in regex_dict.keys():
		result[key] = dict()
	
	#Iterate over files disassembled looking for regex matches
	for root, dirs, files in os.walk(output_directory):
		for file in files:
			if file.endswith('.smali') or file.endswith('.xml'):
				for key, value in regex_dict.iteritems():
					file_full_path = os.path.join(root, file)
					strings = re.findall(value, open (file_full_path, 'r').read())
					if(len(strings) > 0):
						result[key][file_full_path] = strings
				
	#Dump to report file
	for key1 in regex_dict.keys():
		printBanner(report, key1)
		for key2, value2 in result[key1].iteritems(): 
			report.write(key2 + '\n\t' + '\n\t'.join(value2) + '\n\n')
		
	report.close()


if __name__ == "__main__":
	
	if(len(sys.argv) == 2 and sys.argv[1].endswith(".apk") and os.path.isfile(sys.argv[1])):
		analyze(sys.argv[1], 'output-'+sys.argv[1]+'/content/', 'output-'+sys.argv[1]+'/report.txt')
		
	else:
		print '\nInvalid parameters or the file it\'s not accessible.\n\nUsage: analyze.py file.apk\n'
		sys.exit(0)
		