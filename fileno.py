#!/usr/bin/env python3.2
import os,sys

if len(sys.argv) < 2:
	print("Usage: %s dirpath" % sys.argv[0])
	sys.exit()

path = sys.argv[1]
filenum = 0
cnum = 0
hnum = 0
snum = 0

for root, dirs, files in os.walk(path, topdown=True):
	filenum += len(files)
	for name in files:
		if name[-2:] == '.c':
			cnum += 1
		if name[-2:] == '.h':
			hnum += 1
		if name[-2:] == '.S':
			snum += 1

print("Toltal %d files in %s" % (filenum, path))
print(".c:%d, .h:%d, .S:%d " % (cnum, hnum, snum))
