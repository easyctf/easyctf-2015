import math
import os
import random

operations = [
	{ "name": "add", "func": (lambda a, b: a + b) },
	{ "name": "subtract", "func": (lambda a, b: a - b) }
]

def generate(full_path):
	try:
		for i in range(10):
			operation = random.choice(operations)
			n1 = random.randint(1, 1000)
			n2 = random.randint(1, 1000)
			
			f = open(full_path + os.sep + "test" + str(i) + ".in", "w")
			f.write("%s %d %d\n" % (operation["name"], n1, n2))
			f.close()
			
			f = open(full_path + os.sep + "test" + str(i) + ".out", "w")
			f.write("%d\n" % int(abs(operation["func"](n1, n2))))
			f.close()
		return 1
	except:
		return 0