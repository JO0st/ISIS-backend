#!/usr/bin/python

import subprocess
import string
from database import *

def crak(BSSID, wordlist="/usr/share/dict/british-english", file="psk-01.cap"):
	command=["sudo","aircrack-ng","-w"]
	command.append(wordlist)
	command.append("-b")
	command.append(BSSID)
	command.append(file)
	uit=open ("output.txt", "w")
	print command
	proc_aircrack=subprocess.Popen(command, stdout=uit, stderr=uit)
	proc_aircrack.wait()
	uit.close()

def process_output():
	file=open ("output.txt", "r")
	key="-1"
	text=""
	for line in file:
		if "KEY FOUND" in line and key=="-1":
			key=line[24:-7]
	return key

def post(ESSID, key):
	if key!="-1":
		query= "update ap_info set wifi_key = '"
		query+=key
		query+="' where wifi_network = '"
		query+=ESSID
		query+="';"
		xecutequery(query)
	else:
		raise Exception("cracking failed") 

def automate(BSSID, ESSID, file="psk-01.cap"):
	crak(BSSID)
	key=process_output()
	post(ESSID, key)

if __name__ == '__main__':
	crak("00:21:91:04:B9:25")
	process_output()