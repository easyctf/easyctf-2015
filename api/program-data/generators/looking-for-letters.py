import math
import os
import random

import imp
common = imp.load_source("common", "/home/easyctf/easyctf/api/program-data/generators/common.py")

def insert(original, new, pos):
	return original[:pos] + str(new) + original[pos:]

def generate(full_path):
	try:
		chosen = random.sample(set(common.strings), 10)
		changed = chosen
		orig = chosen
		for i in range(10):
			output = chosen[i] + "\n"
			f = open(full_path + os.sep + "test" + str(i) + ".out", "w")
			f.write("%s" % output)
			f.close()
			for b in range(20):
				changed[i] = insert(changed[i], random.randint(0,9), random.randint(0,len(changed[i])-1))
			name = changed[i]
			f = open(full_path + os.sep + "test" + str(i) + ".in", "w")
			f.write("%s\n" % name)
			f.close()
			
		return 1
	except:
		return 0