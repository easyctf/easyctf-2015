import math
import os
import random
import string

import traceback

import imp
common = imp.load_source("common", "/home/easyctf/easyctf/api/program-data/generators/common.py")

def generate(full_path):
	try:
		chosen = random.sample(set(common.sentences), 10)
		for i in range(10):
			sentence = chosen[i]
			newsentence = ""
			for j in range(len(sentence)):
				if sentence[j] in (string.ascii_uppercase + string.ascii_lowercase) and random.randint(1, 2) == 2:
					newsentence += chr(ord(sentence[j]) ^ 32)
				else:
					newsentence += sentence[j]
			sentence = newsentence
			inverted = ""
			for j in range(len(sentence)):
				c = sentence[j]
				if c in (string.ascii_uppercase + string.ascii_lowercase):
					inverted += chr(ord(c) ^ 32)
				else:
					inverted += sentence[j]
			
			f = open(full_path + os.sep + "test" + str(i) + ".in", "w")
			f.write("%s\n" % inverted)
			f.close()
			
			f = open(full_path + os.sep + "test" + str(i) + ".out", "w")
			f.write("%s\n" % sentence)
			f.close()
		return 1
	except:
		traceback.print_exc()
		return 0