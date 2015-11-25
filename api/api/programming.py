# THIS FILE IS UNUSED, HERE FOR HISTORICAL REASONS
# Use https://github.com/EasyCTF/easyctf-2015-judge to judge things

import filecmp
import imp
import os
import os.path
import shutil
import locale
import traceback
from threading import Timer
import subprocess

import api
from api.exceptions import *

from datetime import datetime

extensions = {
	"c": "c",
	"java": "java",
	"python2": "py",
	"python3": "py"
}

"""
signals:
- c: Didn't compile or compiled with an error
- e:
  - 1: Generator screwed up
  - 2: Generator is missing
- l: Language not implemented
- m: Program is missing
- t: Program timed out
"""

def program_return(token, signal, message):
	db = api.common.db_conn()
	pid = db.programs.find_one({ "token": token })["pid"]
	update = {
		"done": True,
		"signal": signal,
		"message": message,
		"log": open("/programs" + os.sep + token + os.sep + "stdout.log").read()
	}
	if update["signal"] == "*":
		flag = db.problems.find_one({ "pid": pid })["flag"]
		update["flag"] = flag
	db.programs.update_one({ "token": token }, { "$set": update })
	os.chdir("/home/easyctf/easyctf")
	shutil.rmtree("/programs" + os.sep + token)
	# to be implemented

def touch(fname, times=None):
	with open(fname, 'a'):
		os.utime(fname, times)
	
def debug(fullpath, message):
	os.setuid(1000)
	os.setgid(1000)
	f = open(fullpath, "a")
	f.write("%s\n" % message)
	f.close()

def run_program(token, language):
	os.chdir("/home/easyctf/easyctf")
	db = api.common.db_conn()
	doc = db.programs.find_one({ "token": token })
	
	basedir = "/programs" + os.sep + token
	envdir = basedir + os.sep + "env"
	datadir = basedir + os.sep + "data"
	logfile = basedir + os.sep + "stdout.log"
	
	# create output file
	# open(logfile, "w")
	# os.chmod(logfile, 660)
	# os.chown(logfile, 1001, 1000)
	subprocess.call("sudo -u user touch " + logfile, shell=True)
	subprocess.call("sudo chown user:easyctf " + basedir + os.sep + "stdout.log", shell=True)
	subprocess.call("sudo chmod 664 " + basedir + os.sep + "stdout.log", shell=True)
	
	# verify upload
	debug(logfile, "Locating program...")
	filename = envdir + os.sep + "program." + extensions[language]
	if not os.path.exists(filename):
		return program_return(token, "m", "Program is missing")
	debug(logfile, "Located program.\n")
	
	# switch user to program
	# os.setgid(1001)
	# os.setuid(1001)
	
	Timer(80, program_return, (token, "t", "Program ran too long."))
	subprocess.call("sudo chown -R user:user " + envdir, shell=True)
	subprocess.call("sudo chmod -R 0777 " + envdir, shell=True)
	
	# compile program
	debug(logfile, "Compiling program...")
	original_cwd = os.getcwd()
	os.chdir(envdir)
	print(os.getcwd())
	if language == "c":
		program_return(token, "l", "Language not implemented")
		return
	elif language == "java":
		try:
			output = subprocess.check_output("sudo -u user javac " + filename, shell=True)
			debug(logfile, "Compiled.\n")
		except subprocess.CalledProcessError as error:
			debug(logfile, "Failed to compile.\n")
			debug(logfile, error.output.decode(encoding="UTF-8"))
			program_return(token, "c", "Didn't compile or compiled with an error. Check your syntax.")
			return
	elif language == "python3":
		try:
			output = subprocess.check_output("sudo -u user python3 -m py_compile " + filename, shell=True)
			debug(logfile, "Compiled.\n")
		except subprocess.CalledProcessError as error:
			# shiet
			debug(logfile, "Failed to compile.\n")
			debug(logfile, error.output.decode(encoding="UTF-8"))
			program_return(token, "c", "Didn't compile or compiled with an error. Check your syntax.")
			return
	elif language == "python2":
		try:
			output = subprocess.check_output("sudo -u user python -m py_compile " + filename, shell=True)
			debug(logfile, "Compiled.\n")
		except subprocess.CalledProcessError as error:
			# shiet
			debug(logfile, "Failed to compile.\n")
			debug(logfile, error.output.decode(encoding="UTF-8"))
			program_return(token, "c", "Didn't compile or compiled with an error. Check your syntax.")
			return
	os.chdir(original_cwd)
		
	# generate inputs/outputs
	debug(logfile, "Generating inputs...")
	try:
		generator = imp.load_source(doc["pid"], api.config.basedir + os.sep + "api" + os.sep + "program-data" + os.sep + "generators" + os.sep + doc["pid"] + ".py")
	except Exception as e:
		program_return(token, "e", "An error occurred (2). Please notify an admin immediately.")
		debug(logfile, "Could not open generator %s.\n" + e.output.decode(encoding="UTF-8"))
		return
	if "generate" in dir(generator):
		result = generator.generate(datadir)
		if result == 0:
			program_return(token, "e", "An error occurred (1). Please notify an admin immediately.")
			debug(logfile, "Generation failed.\n")
			return
		else:
			debug(logfile, "Generated inputs.\n")
	else:
		program_return(token, "e", "An error occurred (2). Please notify an admin immediately.")
		debug(logfile, "Could not open generator.\n")
		return

	print(os.listdir(envdir))

	subprocess.call("sudo chmod -R 700 " + datadir, shell=True)
	
	# allow writing
	subprocess.call("sudo chmod 0777 " + envdir, shell=True)
		
	for i in range(10):
		# os.setuid(1000)
		# os.setgid(1000)
		try:
			print(os.popen("id").read())
			print(os.getcwd())
			# copy input file to env folder
			debug(logfile, "Loading test " + str(i+1) + "...\n")
			testfile = datadir + os.sep + "test" + str(i) + ".in"
			print(os.listdir(datadir))
			if os.path.exists(testfile):
				testtarget = envdir + os.sep + doc["pid"] + ".in"
				if os.path.exists(testtarget): subprocess.call("sudo rm " + testtarget, shell=True)
				print(os.listdir(envdir))
				shutil.copyfile(testfile, testtarget)
				subprocess.call("sudo chown -R user:easyctf " + testtarget, shell=True)
			subprocess.call("sudo chown -R user:user " + envdir, shell=True)
		except Exception as e:
			program_return(token, "0", "Error({0}): {1}".format(e.errno, e.strerror))
		
		# os.setuid(1001)
		# os.setgid(1001)
		debug(logfile, "Running test " + str(i+1) + "...\n")
		try:
			if language == "c":
				program_return(token, "l", "Language not implemented")
			elif language == "java":
				output = subprocess.check_output("sudo -u user java program", shell=True, cwd=envdir, timeout=1, stderr=subprocess.STDOUT)
				output = "\n".join([(">>> " + x) for x in (output.decode("utf-8")).split("\n")])
				debug(logfile, "Program output:\n" + output)
			elif language == "python2":
				output = subprocess.check_output("sudo -u user python program.py", shell=True, cwd=envdir, timeout=1, stderr=subprocess.STDOUT)
				output = "\n".join([(">>> " + x) for x in (output.decode("utf-8")).split("\n")])
				debug(logfile, "Program output:\n" + output)
			elif language == "python3":
				output = subprocess.check_output("sudo -u user python3 program.py", shell=True, cwd=envdir, timeout=1, stderr=subprocess.STDOUT)
				output = "\n".join([(">>> " + x) for x in (output.decode("utf-8")).split("\n")])
				debug(logfile, "Program output:\n" + output)
		except subprocess.TimeoutExpired as error:
			program_return(token, "t", "Program timed out.")
			return
		except subprocess.CalledProcessError as error:
			program_return(token, "b", "Program crashed: " + error.output.decode(encoding="UTF-8"))
			return
		except Exception as error:
			program_return(token, "e", "Unknown error: " + error.output.decode(encoding="UTF-8"))
			return
			
		# os.setuid(1000)
		# os.setgid(1000)
		
		# compare outputs
		actualoutput = envdir + os.sep + doc["pid"] + ".out"
		if not(os.path.exists(actualoutput)):
			debug(logfile, "Output not found.")
			program_return(token, "o", "Your program didn't produce an output (%s.out)." % doc["pid"])
			return
		
		correctoutput = datadir + os.sep + "test" + str(i) + ".out"
		if filecmp.cmp(actualoutput, correctoutput):
			debug(logfile, "Test " + str(i+1) + " correct!\n")
			print("***Test %d completed!***" % (i+1))
			continue
		else:
			debug(logfile, "Test " + str(i+1) + " wrong.\n")
			debug(logfile, "Program input:")
			debug(logfile, repr(open(testfile).read()))
			debug(logfile, "Expected output:")
			debug(logfile, repr(open(correctoutput).read()))
			debug(logfile, "Your program output:")
			debug(logfile, repr(open(actualoutput).read()))
			program_return(token, "x", "You got the problem wrong. Check the log for details.")
			return
		print ("FINISHED")
		
	# dude nice
	debug(logfile, "Congratulations! You've correctly solved " + doc["pid"] + "!")
	program_return(token, "*", "Correct!")
	return
