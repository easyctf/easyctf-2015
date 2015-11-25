import math
import os
import random

def generate(full_path):
	try:
		for i in range(10):
			output = "Hello, EasyCTF!\n"
			f = open(full_path + os.sep + "test" + str(i) + ".in", "w")
			f.write("")
			f.close()
			f = open(full_path + os.sep + "test" + str(i) + ".out", "w")
			f.write("%s" % output)
			f.close()
		return 1
	except:
		return 0