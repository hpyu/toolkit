#!/usr/bin/env python
##
# This script make anki card from pdf copied englishpod docs
##

__metatype__ = type # new type class
class ep_to_anki:
	def __init__(self):
		self.lines = []
		self.full = []
		self.eppath = "/home/hpyu/tmp/ep/"
		self.fname = os.path.abspath(sys.argv[1])
		self.lessons = {}
	
	def load_and_ajust_lines(self):
		f = open(self.fname)
		## load lines and remove blank lines and page number lines
		for l in f.readlines():
			#printf("len %d, %s" % (len(l),l))
			if len(l) > 4:
				self.lines.append(l)

		## align title
		printf("total line %d " % len(self.lines))
		i = 0;
		while i < len(self.lines) - 1:
			#printf("i:%d :%s" % (i, self.lines[i]))
			if "  -  " in self.lines[i]:
				if "(" not in self.lines[i]:
					subject = self.lines[i][:-2] + self.lines[i+1]
					self.full.append("\n### ")
					self.full.append(subject)
					i += 1
				else:
					self.full.append("\n### ")
					self.full.append(self.lines[i])
				i += 1
			elif ':' in self.lines[i]:
				if ':' in self.lines[i+1]:
					self.full.append(self.lines[i])
					i += 1
				else: 
					j = i+1
					sentence = self.lines[i]
					while ':' not in self.lines[j]:
						if "  -  " in self.lines[j]:
							break
						sentence = sentence[:-2] + self.lines[j]
						j += 1
					i += 1
					self.full.append(sentence)
			else:
				i += 1
				
		f.close()

	def save_to_file(self):
		fnorm = open(os.path.join(self.eppath,"ep_full.txt"), "w")
		for i in range(len(self.full)):
			fnorm.write("%s" % self.full[i])
		fnorm.close()

		fanki = open(os.path.join(self.eppath,"ep_anki.txt"), "w")
		for i in range(len(self.full)):
			if '###' in self.full[i]:
				subject = '[' + self.full[i+1][:-2] +']'
				fanki.write("\n")

			if '###' not in self.full[i] and '  -  ' not in self.full[i]:
				context = self.full[i][:-2]+"\t"+ subject + "\n"
				fanki.write("%d\t %s" % (i,context))
		fanki.close()

	def save_to_each_file(self):
		i = 0
		while i < len(self.full):
			if i < len(self.full) and "###" in self.full[i]:
				line = self.full[i+1]
				line = line.strip()
				title = line[:-1].replace(' ', '_')
				title = title.replace('(', '')
				title = title.replace('__', '')
				title = title[-4:] + '_' + title + '.txt'
				fname = os.path.join(self.eppath, title)
				printf("Create: %s" % fname)
				f = open(fname, 'w')
				j = i + 2
				while j < len(self.full) and "###" not in self.full[j]:
					f.write("%d\t %s" % (j,self.full[j]))
					j += 1
				else:
					f.close()
					i = j
			else:
				i += 1

			
			
	
def main():
	w = ep_to_anki()
	w.load_and_ajust_lines()
	w.save_to_file()
#	w.save_to_each_file()

if __name__ == '__main__':
	# Python2.x & 3.x compatible
	from distutils.log import warn as printf
	from os.path import *
	import os,sys,shutil
	main()

