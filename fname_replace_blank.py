# hpyu: 2015.01.7
# replace the blank in fname with '_'

#!/usr/bin/env python3.2
import os, sys, fnmatch

def walk(path):
	cur_path = os.path.abspath(path)
	#print(cur_path + ":")
	for name in os.listdir(cur_path):
		'''
		if os.path.isdir(os.path.join(cur_path, name)):
			print("d :" + name)
		else:
			print("f :" + name)
		'''
		if fnmatch.fnmatch(name, "* *"):
			print("fname with blank: %s" % name);
			new_name = name.replace(" ", "_")
			os.rename(os.path.join(cur_path, name), os.path.join(cur_path, new_name))
			name = new_name
			print("fname with blank: %s" % name);

		if os.path.isdir(os.path.join(cur_path, name)):
			walk(os.path.join(cur_path, name))
			

walk(sys.argv[1])


