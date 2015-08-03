#!/usr/bin/env python3.2

import os,sys,string,fileinput

if len(sys.argv) < 2:
	print("Usage %s patch_file\n", sys.argv[0])
	sys.exit()

fname = os.path.abspath(sys.argv[1])
head = []


#1. try to merge patch
msg = os.popen("patch -p1 < " + fname).readlines()
print(msg)
for line in msg:
	if (line.find(" FAILED at ") != -1 or 
	line.find("can't find file") != -1 or 
	line.find("patch existed!") != -1):
		print("Merge patch failed!!!\n")
		print("git reset --hard\n")
		os.system("git reset --hard")
		sys.exit()

#2. make commit
for line in  fileinput.input(fname):
	if (len(line) == 4 and line[:3] == "---"):
		break
	if (line[:7] == "Subject"):
		index = line.find("] ")
		title = line[index+2:]
	head.append(line)

print("title: %s" % title)
print("head:")
for line in head:
	print(line[:-1])

#3 commit to git
os.system("git add -u")
fd_msg = open("git_msg", 'w')
fd_msg.writelines(title)
fd_msg.writelines("\n")
fd_msg.writelines(head)
fd_msg.close()

os.system("git commit --file git_msg")

