import math
import os
import random
import string


	
def makeid():
    text = "";
    possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

    for i in range(30):
        text += possible[math.floor(random.random() * len(possible))];

    return text;
    

def strChanger(s,a):
	sList = list(s)
	for x in a:
	    for i in range(len(s)):
	        if i+1 < len(s) and (i+1)%x == 0:
	            if ord(sList[i+1]) < 122 and ord(sList[i+1]) >= 90:
	                sList[i+1] = chr(ord(sList[i+1])+1)
	            elif ord(sList[i+1]) == 122:
	                sList[i+1] = chr(97)
	            elif ord(sList[i+1]) < 90 and ord(sList[i+1]) >= 65:
	                sList[i+1] = chr(ord(sList[i+1])+1)
	            elif ord(sList[i+1]) == 90:
	                sList[i+1] = chr(65)
	newS = "".join(sList)
	return newS


def generate(full_path):
	try:
		randString = ""
		numList = list()
		for a in range(5):
			num = random.randint(2,20)
			numList.append(num)
		for i in range(10):
			randString = makeid()
			f = open(full_path + os.sep + "test" + str(i) + ".in", "w")
			f.write(",".join([str(j) for j in numList]) + "\n" + randString + "\n")
			f.close()

			output = strChanger(randString,numList) + "\n"
			f = open(full_path + os.sep + "test" + str(i) + ".out", "w")
			f.write("%s" % output)
			f.close()
			randString = ""
		return 1
	except:
		return 0