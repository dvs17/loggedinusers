#!/usr/bin/python
import subprocess, os, argparse, time, datetime, socket, base64, threading, Queue, hashlib, binascii, signal, sys, getpass
from optparse import OptionParser
import re
from subprocess import check_output
from subprocess import PIPE
import shlex
import fileinput
def validate(dafile,domain,username,password,file):
	try:
		if len(password) < 64:
			cmd = ("cme smb -u {} -p {} -d {} {} --loggedon-users | tr -d '\\000' | grep 'logon_server:' | grep -v 'NT AUTHORITY'").format(username, password, domain, file)
			proc = os.popen(cmd).readlines()
			for x in proc:
				x = filter(None, x)
				ip = x.strip().split()[1].split(":")[0]
				user = x.strip().split()[4].split("\\")[1]
				with open(dafile, "r") as f:
					lines = f.read()
					lines = lines.split()
					lines = "(" + ")|(".join(lines) + ")"
					if re.match(lines , user , re.IGNORECASE):
						print "\033[96m"+ip+"\t"+user+"\033[96m"+" (Administrator!!!)"
					else:
						print ip+"\t"+user, "(Basic User)"
					if user.lower() in lines.lower():
						print ip+"\t"+user, "(Interesting User?)"
					
		elif len(password) > 64:
			cmd = ("cme smb -u {} -H {} -d {} {} --loggedon-users | tr -d '\\000' | grep 'logon_server:' | grep -v 'NT AUTHORITY'").format(username, password, domain, file)
			proc = os.popen(cmd).readlines()
			for x in proc:
				x = filter(None, x)
                                ip = x.strip().split()[1].split(":")[0]
				user = x.strip().split()[4].split("\\")[1]
                                with open(dafile, "r") as f:
                                        lines = f.read()
                                        lines = lines.split()
                                        lines = "(" + ")|(".join(lines) + ")"
                                        if re.match(lines , user , re.IGNORECASE):
                                                print "\033[96m"+ip+"\t"+user+"\033[96m"+" (Administrator!!!)"
                                        else:
                                                print ip+"\t"+user, "(Basic User)"
					if user.lower() in lines.lower():
						 print "\033[96m"+ip+"\t"+user+"\033[96m"+" (Interesting User?)"

	except socket.error as e:
		return False

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', '--username', help='Enter Domain User')
	parser.add_argument('-p', '--password', help='Enter Domain password')
	parser.add_argument('-d', '--domain', help='Enter Domain name')
	parser.add_argument('-f', '--file', help='List if hosts')
	parser.add_argument('-da', '--dafile', help='Domain Admins file list[create empty file to ignore this function]')
	args = parser.parse_args()
	if args.file:
		with open (args.file) as f:
	               lines = validate(args.dafile, args.domain, args.username, args.password, args.file)
if __name__ == '__main__':
	main()
