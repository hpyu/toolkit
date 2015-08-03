# hpyu 20120122 split dumpstate log to seperated files for each item

#!/usr/bin/env python3.2

import os,sys,re,shutil,string

print("-----------------------------------\n")
if len(sys.argv) < 3:
	print("Usage %s dumpstate dir\n", sys.argv[0])
	sys.exit()

fname = os.path.abspath(sys.argv[1])
dname = os.path.abspath(sys.argv[2])

if os.path.exists(dname):
	print("%s exists" % dname)
	if input('remove it?') not in ['y', 'Y']:
		sys.exit()
	else:
		shutil.rmtree(dname)
		

print("----- recreate %s ----\n" % dname)
os.mkdir(dname)
os.system('cp -v {} {}'.format(fname, dname))

dsfile = open(fname,'r', errors='ignore')
log = dsfile.readlines()
print(len(log))
pos = []
for i in range(0, len(log)):
	line = log[i]
	if line[:7] == '------ ':
		pos.append(i)

pos.append(len(log))

fsched = False
fshowmap = False

for i in range(0, len(pos)-1):
	line = log[pos[i]]

	item = line[7:-8]
	if item[:5] == 'SCHED':
		if fsched == False:
			name = '{0:d}_SCHED.txt'.format(i)
			print(name)
			fsched = open(os.path.join(dname,name), 'w')
			
		fsched.writelines(log[pos[i]:pos[i+1]])
	elif item[:8] == "SHOW MAP":
		if fshowmap == False:
			name = '{0:d}_show_map.txt'.format(i)
			print(name)
			fshowmap = open(os.path.join(dname,name), 'w')
		fshowmap.writelines(log[pos[i]:pos[i+1]])
	else:
		for c in ['(', ')', ':', '/', '.', ' ','*']:
			item = item.replace(c, '_')
		if len(item) > 80:
			item = item[:80]
		name = '{:-d}_{}.txt'.format(i,item)
		print(name)
		f = open(os.path.join(dname,name), 'w')
		f.writelines(log[pos[i]:pos[i+1]])
		f.close()

fsched.close()
fshowmap.close()

		
	

