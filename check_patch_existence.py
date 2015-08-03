#!/usr/bin/env python3.2

# hpyu: 2015.01.14
# checking if patch merged in backdelivery code
# run it in backdelivery root dir 

import os,sys

'''
### failed to merge
1. confilct
Hunk #1 FAILED at 262.
1 out of 1 hunk FAILED -- saving rejects to file drivers/clk/mmp/dvfs-pxa1908.c.rej

2, can't find file to patch, maybe kernel dir issue
can't find file to patch at input line 20

3, patch existed
patch detected!

### succeed to merge
4, patch can be merged, means patch missed
not aboove error and  have "succeeded"

5, only print
patching file arch/arm64/mach/pxa1908_lowpower.c
'''

failed_list = []
nofile_list = []
exist_list  = []
missed_list = []


def check_one_patch(patch):
	os.system("git reset --hard")
#	print("1111111111111111111111111111111111111111111111111111")
	cmd = "patch -p1 < " + patch
	msg = os.popen(cmd).readlines()

#	for line in msg:
#		print(line)

	for line in msg:
		if line.find("FAILED") != -1:
#			print("xxxxxxxx add to failed_list");
			failed_list.append(patch)
			return
		elif line.find("can\'t find file") != -1:
#			print("xxxxxxxx add to nofile_list");
			nofile_list.append(patch)
			return
		elif line.find("patch existed!") != -1 or line.find("patch detected!") != -1:
#			print("xxxxxxxx add to exist_list");
			exist_list.append(patch)
			return

	missed_list.append(patch)
		
#	print("2222222222222222222222222222222222222222222222222222")

def check_patches(path):
	files = os.listdir(path)
	files.sort(key=lambda x:int(x[:4]))
	for name in files:
		print(name)
	
	for name in files:
		check_one_patch(os.path.join(path, name))


def main():
	if len(sys.argv) < 2:
		print("Usage %s patches_dir\n", sys.argv[0])
		sys.exit()

	path = os.path.abspath(sys.argv[1])

	check_patches(path)

	print("\nFailed patches are:\n")
	for name in failed_list:
		print(name)
	
	print("\ncan't find file patches are:\n")
	for name in nofile_list:
		print(name)
	
	print("\nexisted patches are:\n")
	for name in exist_list:
		print(name)
	
	print("\nmissed patches are:\n")
	for name in missed_list:
		print(name)	

main()

