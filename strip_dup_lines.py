#!/usr/bin/env python3.2

import os,sys,fileinput

if len(sys.argv) < 2:
	print("Usage %s infile\n", sys.argv[0])
	sys.exit()

fname = sys.argv[1]
nonredundant_list = []

with fileinput.input(fname) as f:
	for line in f:
		if line not in nonredundant_list:
			nonredundant_list.append(line)

for line in nonredundant_list:
	print(line,end='')

