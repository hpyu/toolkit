#!/usr/bin/env python

__metatype__ = type # new type class
class crash_wrapper:
	def __init__(self):
		self.rawdump = []
		self.elfdump = ''
		self.crash_cmd = ''
		self.dumptype = ''
	
	def check_vmlinux(self):
		if 'vmlinux' not in os.listdir(os.path.curdir):
			printf("vmlinux missed!")
			sys.exit()
	
	def get_rawdump_list(self):
		for fname in os.listdir(os.path.curdir):
			sizeMB = os.path.getsize(fname) >> 20
			if fname[:8] == 'ap_sdram' and fname[-4:] == '.lst':
				if sizeMB < 512:
					printf("ramdump file %s is probaly broken" % fname)
				self.rawdump.append(fname)
				self.dumptype = 'raw'

		for i in range(len(self.rawdump)):
			printf(self.rawdump[i])

	def get_elfdump(self):
		for fname in os.listdir(os.path.curdir):
			sizeMB = os.path.getsize(fname) >> 20
			if sizeMB > 511:
				ftype = os.popen('file ' + fname)
				if 'ELF' in ftype.read():
					printf("ELF dump found :%s" % fname)
					self.elfdump = fname
					self.dumptype = 'elf'
					break

	def make_cmd(self):
		if self.dumptype == 'raw':
			for ramname in self.rawdump:
				offset = ramname.split('-')[0].split('_')[-1]
				self.crash_cmd += ramname+'@'+offset+','
			self.crash_cmd = "crash64 "+self.crash_cmd+' vmlinux'
		elif self.dumptype == 'elf':
			self.crash_cmd = 'crash64 '+self.elfdump+' vmlinux'
		
		printf(self.crash_cmd)

	def open_dump(self):
		output = os.system(self.crash_cmd)
#		printf(output.read())
			
def main():
	w = crash_wrapper()
	w.check_vmlinux()
	w.get_rawdump_list()
	if w.dumptype == '':
		w.get_elfdump()

	if w.dumptype == '':
		printf("No dump found!!!!\n")
		sys.exit()
		
	w.make_cmd()
	w.open_dump()

if __name__ == '__main__':
	# Python2.x & 3.x compatible
	from distutils.log import warn as printf
	from os.path import *
	import os,sys,shutil
	main()

