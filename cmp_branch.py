#!/usr/bin/env python

__metatype__ = type # new type class
class wraper:
	def __init__(self):
		self.plist = [[],[]]
		self.plist_diff = [[],[]]
		self.phash = [{},{}]
		self.bname = {}
		self.fname = {}
		self.cnum = {}
		self.bname[0] = sys.argv[1].split(',')[0].split(':')[0]
		self.bname[1] = sys.argv[1].split(',')[1].split(':')[0]
		self.cnum[0] = sys.argv[1].split(',')[0].split(':')[1]
		self.cnum[1] = sys.argv[1].split(',')[1].split(':')[1]
		self.fname[0] = "%s_%s_commits.txt" % (self.bname[0], self.cnum[0])
		self.fname[1] = "%s_%s_commits.txt" % (self.bname[1], self.cnum[1])
	
	def save_list_to_file(self, filename, listname):
		f = open(filename,'w')
		for line in listname:
			f.writelines(line)
			f.writelines("")
		f.close()

	def get_commits(self):
		for i in [0, 1]:
			cmd = "git log %s --graph --pretty=format:\'%%h %%s\' --abbrev-commit -%s > %s"\
				% (self.bname[i], self.cnum[i], self.fname[i])

			printf("cmd: %s" % cmd)
			msg = os.popen(cmd)
			printf(msg)
	
			f = open(self.fname[i], 'r')
			printf("================== %s =================" % self.fname[i])
			for line in f.readlines():
				cid = line.split(" ", 2)[1] 	#commit id
				csbj = line.split(" ", 2)[2]	#commit subject
				self.plist[i].append("%s %s" % (cid, csbj))
				self.phash[i].setdefault(csbj, cid)

			self.save_list_to_file(self.bname[0]+"_list_0.txt", self.plist[0])
			self.save_list_to_file(self.bname[1]+"_list_1.txt", self.plist[1])
			self.save_list_to_file(self.bname[0]+"_hash_0.txt", list(self.phash[0].keys()))
			self.save_list_to_file(self.bname[1]+"_hash_1.txt", list(self.phash[1].keys()))
#			for sbj in self.plist[i]:
#				print("%d list %s " % (i,sbj))
#				
#			for sbj in list(self.phash[i].keys()):
#				print("%d hash %s " % (i,sbj))

	def get_diff(self):
		self.plist_diff[0].extend(self.plist[0])
		self.plist_diff[1].extend(self.plist[1])

		for line in self.plist[0]:
			sbj = line.split(" ", 1)[1]
			if self.phash[1].has_key(sbj):
				self.plist_diff[0].remove(line)
			
		for line in self.plist[1]:
			sbj = line.split(" ", 1)[1]
			if self.phash[0].has_key(sbj):
				self.plist_diff[1].remove(line)

		self.save_list_to_file(self.bname[0]+"_diff_0.txt", self.plist_diff[0])
		self.save_list_to_file(self.bname[1]+"_diff_1.txt", self.plist_diff[1])


def main():

	if (len(sys.argv) < 2):
		printf("Usage: python %s branch1:cnum1,branch2:num2" % sys.argv[0])
		sys.exit("invalid params")
	
	p = wraper()

	p.get_commits()
	p.get_diff()
	

if __name__ == '__main__':
	# Python2.x & 3.x compatible
	from distutils.log import warn as printf
	from os.path import *
	import os,sys,shutil,getopt
	main()

