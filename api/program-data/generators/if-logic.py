import math
import os
import random

def generate(full_path):
	try:
		numList = list()
		strList = list()
		for i in range(10):
			for a in range(25):
				num = random.randint(0,200)
				numList.append(num)
			f = open(full_path + os.sep + "test" + str(i) + ".in", "w")
			f.write("%s\n" % ",".join([str(j) for j in numList]))
			f.close()
			for b in numList:
				if b >= 0 and b <= 50:
					strList.append("hi\n")
				elif b > 50 and b <= 100:
					strList.append("hey\n")
				else:
					strList.append("hello\n")
			output = "%s" % "".join([str(j) for j in strList])
			f = open(full_path + os.sep + "test" + str(i) + ".out", "w")
			f.write("%s" % output)
			f.close()
			numList = []
			strList = []
		return 1
	except:
		return 0