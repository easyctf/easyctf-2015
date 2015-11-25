import os
import os.path
import shutil
import json

import api
import api.common
import api.config

db = api.common.db_conn()

# wipe

db.problems.remove({})

# insert

problem_dir = "/srv/http/ctf/static/problems"
load_dir = api.config.basedir + "/api/problems"

categories = os.listdir(load_dir)
if os.path.exists(problem_dir):
	shutil.rmtree(problem_dir)
os.makedirs(problem_dir)

for category in categories:
	category_count = 0
	problem_dirs = os.listdir(load_dir + os.sep + category)
	for problem in problem_dirs:
		path = load_dir + os.sep + category + os.sep + problem + os.sep
		try:
			data = json.loads(open(path+problem+".json").read())
			data["successes"] = 0
			db.problems.insert(data)
#			print("- " + problem)
			category_count += 1
			if os.path.exists(path+"static") and os.path.isdir(path+"static"):
				target = problem_dir + os.sep + problem
#				for filename in os.listdir(path+"static"):
#					print("  - " + filename)
				shutil.copytree(path+"static", target)
		except Exception as e:
			print("Failed to load: " + problem + " (" + str(e) + ")")
	print ("%s: %d problems" % (category, category_count))

submissions = db.submissions.find({ "correct": True })
problems = db.problems.find({})
solved = {}

for submission in submissions:
	for problem in problems:
		if problem["pid"] == submission["pid"]:
			if problem["pid"] in solved:
				solved[problem["pid"]] += 1
			else:
				solved[problem["pid"]] = 1
			break

for pid in solved:
	db.problems.update_one({ "pid": pid }, { "$set": { "successes": solved[pid] } })

db.e_problems.remove({})

eastereggs = json.loads(open(api.config.basedir + "/api/eastereggs.json").read())
db.e_problems.insert_many(eastereggs)

print ("> Done loading problems.")