import imp
import threading

import api.auth
import api.common
import api.user

from datetime import datetime
from pymongo.errors import DuplicateKeyError

from api.exceptions import *

basepath = "/home/user/yourctf/api/problems/"

def get_solved_problems(tid=None, uid=None, category=None):
	return [get_problem(pid=pid) for pid in get_solved_pids(tid=tid, uid=uid, category=category)]

def get_solved_pids(tid=None, uid=None, category=None):
	submissions = get_submissions(tid=tid, uid=uid, category=category, showadmin=False, correct=True)
	x = list(set([sub["pid"] for sub in filter(lambda x: x['correct'] == True, submissions)]))
	return x
	print ("ASDF" + str(x))
	z = [ ]
	for w in x:
		if w in z:
			continue
		z.append(w)
	return z

def get_problem_value(pid, bonus_place):
	problem = api.problem.get_problem(pid)
	value = problem["value"]
	if bonus_place in [0, 1, 2]:
		value *= 1.0 + problem["bonus_points"][bonus_place]
	return value

def get_total_count():
	db = api.common.db_conn()
	return db.problems.count()

@api.cache.memoize(timeout=540)
def get_max_points():
	problems = get_all()
	total = 0
	for problem in problems:
		total += get_problem_value(problem["pid"], 0)
	return total

def get_bonus_place():
	bonus_place = {}
	db = api.common.db_conn()
	user = api.user.get_user()
	submissions = db.submissions.find({ "tid": user["team"], "correct": True })
	for submission in submissions:
		if submission["pid"] not in bonus_place:
			bonus_place[submission["pid"]] = submission["bonus_place"]
	return bonus_place

def get_pids(problems):
	pids = []
	for problem in problems:
		if "pid" in problem:
			pids.append(problem["pid"])
	return pids

def get_unlocked():
	db = api.common.db_conn()
	team = api.team.get_team()
	problems_raw = db.problems.find({}).sort([("value", 1), ("pid", 1)])
	solved = get_solved_pids(tid=team["tid"])
	bonus_place = get_bonus_place()
	problems = []
	for problem in problems_raw:
		# weightmap check
		del problem["_id"]
		if "flag" in problem: del problem["flag"]
		problem["successes"] = len(get_teams_solved(problem["pid"]))
		if problem["pid"] in solved:
			problem["solved"] = True
			if problem["pid"] in bonus_place:
				problem["bonus_place"] = bonus_place[problem["pid"]]
			else:
				problem["bonus_place"] = -1
		else:
			problem["solved"] = False
			score = 0
			for prereq in problem["weightmap"]:
				if prereq in solved:
					score += problem["weightmap"][prereq]
			# if score < problem["threshold"]: continue
			if not("admin" in team and team["admin"] == True):
				if score < problem["threshold"]: continue
		bp = []
		for x in problem["bonus_points"]:
			bp.append(round(x, 2))
		problem["bonus_points"] = bp
		del problem["weightmap"]
		del problem["threshold"]
		problems.append(problem)
	return problems

def get_all():
	db = api.common.db_conn()
	problems = list(db.problems.find({}))
	return problems

def get_problem(pid):
	db = api.common.db_conn()
	problem = db.problems.find_one({ "pid": pid })
	return problem

def get_grader(pid):
	problem = get_problem(pid)
	grader_path = basepath + problem["grader"]
	return imp.load_source(pid, grader_path)

def grade_problem(pid, answer, tid):
	problem = get_problem(pid)
	grader = get_grader(pid)
	
	result = grader.grade(tid, answer)
	return {
		"correct": result["correct"],
		"points": problem["value"],
		"message": result["message"]
	}
	
def e_solved():
	solved = []
	db = api.common.db_conn()
	user = api.user.get_user()
	submissions = db.e_submissions.find({ "tid": user["team"], "correct": True })
	for submission in submissions:
		if submission["pid"] not in solved:
			solved.append(submission["pid"])
	return solved
	
def e_solved_names():
	solved = e_solved()
	db = api.common.db_conn()
	
	names = []
	
	eggs = list(db.e_problems.find({}))
	for egg in eggs:
		if egg["pid"] in solved:
			names.append(egg["title"])
	
	return names

def e_submit(tid, answer, ip=None):
	if answer is None or len(answer) < 1:
		raise WebException("Please submit an egg!")
	db = api.common.db_conn()
	
	user = api.user.get_user()
	eggs = list(db.e_problems.find({}))
	correct = False
	
	for egg in eggs:
		if egg["egg"] == answer:
			if egg["pid"] in e_solved():
				raise WebException("You already submitted this egg!")
			correct = True
			e_submission = {
				"uid": user["uid"],
				"tid": tid,
				"timestamp": datetime.now().timestamp(),
				"pid": egg["pid"],
				"ip": ip,
				"answer": answer,
				"correct": True
			}
			db.e_submissions.insert(e_submission)
			break
	
	if correct:
		return { "correct": 1, "message": "dude nice" }
	else:
		return { "correct": 0, "message": "nop try again" }
		
def submit(tid, pid, answer, ip=None):
	if answer is None or len(answer) < 1:
		raise WebException("Please submit a flag!")
	db = api.common.db_conn()
	if pid not in get_pids(get_unlocked()):
		raise WebException("You can't submit flags for problems you haven't unlocked!")
	solved_pids = get_solved_pids(tid=tid)
	if pid in get_solved_pids(tid=tid):
		raise WebException("You have already solved this problem")
	
	user = api.user.get_user()
	uid = user["uid"]
	result = grade_problem(pid, answer, tid)
	problem = get_problem(pid)
	adminTeam = api.team.is_admin_team(tid)
	
	previous_solves = get_submissions(pid=pid, correct=True)
	if result["correct"]:
		if api.team.is_observer_team(tid) == False and adminTeam == False and len(previous_solves) < 3:
			bonus_place = len(previous_solves)
		else:
			bonus_place = -1
		api.cache.invalid_memoization(get_teams_solved, [ pid ])
	else:
		bonus_place = -1
		
	timestamp = datetime.now().timestamp()
	
	if pid == "survey":
		timestamp = api.config.start_time.timestamp() + 1
	
	submission = {
		"admin": adminTeam == True,
		"uid": uid,
		"tid": tid,
		"timestamp": timestamp,
		"pid": pid,
		"ip": ip,
		"answer": answer,
		"correct": result["correct"],
		"category": problem["category"],
		"bonus_place": bonus_place
	}
	
	if (answer, pid) in [(submission["answer"], submission["pid"]) for submission in get_submissions(tid)]:
		raise WebException("You or one of your teammates already tried this solution.")
	try:
		db.submissions.insert(submission)
	except DuplicateKeyError:
		raise WebException("You or one of your teammates already tried this solution.")
	
	return result

@api.cache.memoize(timeout=120)
def get_teams_solved(pid):
	db = api.common.db_conn()
	submissions = list(db.submissions.find({ "correct": True, "pid": pid, "admin": { "$ne": True } }))
	return [submission["tid"] for submission in submissions]

def get_submissions(pid=None, tid=None, category=None, correct=None, showadmin=False, uid=None):
	db = api.common.db_conn()
	match = { }
	if showadmin:
		match.update({ "admin": True })
	else:
		match.update({ "admin": { "$ne": True } })
	if tid is not None:
		match.update({ "tid": tid })
	if pid is not None:
		match.update({ "pid": pid })
	if category is not None:
		match.update({ "category": category })
	if uid is not None:
		match.update({ "uid": uid })
	
	print (match)
	
	if correct is not None:
		match.update({ "correct": correct })
	# print(match)
	
	return list(db.submissions.find(match, { "_id": 0 }))