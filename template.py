#!/usr/bin/env python

__metatype__ = type # new type class
class crash_wrapper:
	def __init__(self):
		self.rawdump = []
		self.elfdump = ''
	
	def check_vmlinux(self):
		if 'vmlinux' not in os.listdir(os.path.curdir):
			printf("vmlinux missed!")
			sys.exit()
	
def main():
	w = crash_wrapper()
	w.check_vmlinux()

if __name__ == '__main__':
	# Python2.x & 3.x compatible
	from distutils.log import warn as printf
	from os.path import *
	import os,sys,shutil
	main()

