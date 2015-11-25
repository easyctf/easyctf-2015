import math
import os
import random

import imp
common = imp.load_source("common", "/home/easyctf/easyctf/api/program-data/generators/common.py")

def pig_latin(string):
	words = string.split(" ")
	new_words = []
	for word in words:
		if word[0] in "aeiouAEIOU":
			new_words.append(word + "yay")
		else:
			new_words.append(word[1:] + word[0] + "ay")
	return " ".join(new_words)

def generate(full_path):
	try:
		chosen = random.sample(set(common.sentences), 10)
		for i in range(10):
			sentence = chosen[i]
			f = open(full_path + os.sep + "test" + str(i) + ".in", "w")
			f.write("%s\n" % sentence)
			f.close()
			
			output = pig_latin(sentence)
			f = open(full_path + os.sep + "test" + str(i) + ".out", "w")
			f.write("%s\n" % output)
			f.close()
		return 1
	except:
		return 0