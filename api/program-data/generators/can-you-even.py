import math
import os
import random

def generate(full_path):
	try:
		numList = list()
		ctr = 0
		for i in range(10):
			for a in range(10):
				num = random.randint(0,100)
				numList.append(num)
			f = open(full_path + os.sep + "test" + str(i) + ".in", "w")
			f.write("%s\n" % ",".join([str(j) for j in numList]))
			f.close()
			for b in numList:
				if b%2 == 0:
					ctr+=1
			output = str(ctr) + "\n"
			f = open(full_path + os.sep + "test" + str(i) + ".out", "w")
			f.write("%s" % output)
			f.close()
			numList = []
			ctr = 0
		return 1
	except:
		return 0