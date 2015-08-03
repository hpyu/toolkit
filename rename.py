#!/usr/bin/env python

__metatype__ = type # new type class
class rename_files:
	def __init__(self):
		self.path = ""
	
	def do_ep_rename(self, fname):
		if fname.split(".")[-1] == 'mp3':
			s = filter(str.isdigit, fname.split(".")[0])
		else:
			s = filter(str.isdigit, fname)
			
		printf(s)

		newname = os.path.join(self.path, s+"_"+fname)
		return newname
			
	def do_ted_rename(self, fname):
		year = fname.split("-")[0].split("_")[-1]
		if len(year) == 4:
			year += '_'

		newname = year+'_'+fname
		return newname

	def do_all_rename(self, rename_func):
		for fname in os.listdir(self.path):
			fullname = os.path.join(self.path, fname)
			newname = rename_func(fname)
			newname = os.path.join(self.path, newname)
			printf(newname)
			os.rename(fullname, newname)
	
def main():
	rn = rename_files()
	rn.path = os.path.abspath(sys.argv[1])
	printf("path: %s" % rn.path)
	rn.do_all_rename(rn.do_ted_rename)

if __name__ == '__main__':
	# Python2.x & 3.x compatible
	from distutils.log import warn as printf
	from os.path import *
	import os,sys,shutil
	main()



