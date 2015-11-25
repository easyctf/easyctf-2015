import api
import moment
import pymongo

import datetime

from api.common import escape

@api.cache.memoize(timeout=30000)
def get_score(tid=None, uid=None):
	score = sum([problem["value"] for problem in api.problem.get_solved_problems(tid=tid, uid=uid)])
	return score

@api.cache.memoize(timeout=30000)
def get_team_score_progression(tid=None):
	def convert_to_time(time):
		#return time
		m, s = divmod(time, 60)
		h, m = divmod(m, 60)
		return "%d:%02d:%02d" % (h, m, s)
	db = api.common.db_conn()
	team = db.teams.find_one({ "tid": tid })
	indices = [ ]
	
	submissions = list(db.submissions.find({ "tid": team["tid"], "correct": True, "timestamp": { "$lt": api.config.end_time.timestamp() } }).sort("timestamp", 1))
	team["submissions"] = submissions
	team["points"] = 0
	for submission in submissions:
		index = submission["timestamp"] - api.config.start_time.timestamp()
		if not(index in indices):
			indices.append(index)
	counted = [ ]
	indices.sort()
	names = [[ "Time", team["teamname"] ]]
	names.append([ convert_to_time(0) ] + [ 0 ])
	for index in indices:
		frame = [ convert_to_time(index) ]
		if len(team["submissions"]) > 0:
			submission = team["submissions"][0]
			time = submission["timestamp"] - api.config.start_time.timestamp()
			if time == index:
				if submission["pid"] not in counted and not(submission["timestamp"] > api.config.end_time.timestamp()):
					counted.append(submission["pid"])
					team["points"] += api.problem.get_problem_value(submission["pid"], submission["bonus_place"])
				team["submissions"].pop(0)
		frame.append(team["points"])
		names.append(frame)
	last = [ convert_to_time(min(moment.now().date.timestamp(), api.config.end_time.timestamp()) - api.config.start_time.timestamp()) ] + [ team["points"] ]
	names.append(last)
	obj = {
		"points": names,
		"options": {
			"title": "%s Score Progression" % team["teamname"],
			"height": 348,
			"legend": { "position": "top" },
			"hAxis": { "textPosition": "none" }
		}
	}
	if "admin" in team and team["admin"] == True:
		obj["secret"] = "easyctf{h4xxing_th3_c0mpetition_s1t3}"
	return obj

@api.cache.memoize(timeout=30000)
def get_scoregraph(show_admin=False):
	def convert_to_time(time):
		#return time
		m, s = divmod(time, 60)
		h, m = divmod(m, 60)
		return "%d:%02d:%02d" % (h, m, s)
	teams = get_all_team_scores(show_admin=False, show_observer=False)[:6]
	# print (teams)
	db = api.common.db_conn()
	indices = [ ]
	for team in teams:
		submissions = list(db.submissions.find({ "tid": team["tid"], "correct": True, "timestamp": { "$lt": api.config.end_time.timestamp() } }).sort("timestamp", 1))
		team["submissions"] = submissions
		team["points"] = 0
		for submission in submissions:
			index = submission["timestamp"] - api.config.start_time.timestamp()
			if not(index in indices):
				indices.append(index)
	indices.sort()
	names = [[ "Time" ] + [ team["teamname"] for team in teams ]]
	names.append([ convert_to_time(0) ] + [ 0 ] * len(teams))
	counted = { }
	for index in indices:
		frame = [ convert_to_time(index) ]
		for team in teams:
			if len(team["submissions"]) > 0:
				submission = team["submissions"][0]
				time = submission["timestamp"] - api.config.start_time.timestamp()
				if team["tid"] not in counted.keys():
					counted[team["tid"]] = [ ]
				if time == index:
					if not(submission["pid"] in counted[team["tid"]]) and not(submission["timestamp"] > api.config.end_time.timestamp()):
						counted[team["tid"]].append(submission["pid"])
						team["points"] += api.problem.get_problem_value(submission["pid"], submission["bonus_place"])
					team["submissions"].pop(0)
			frame.append(team["points"])
		names.append(frame)
	last = [ convert_to_time(min(moment.now().date.timestamp(), api.config.end_time.timestamp()) - api.config.start_time.timestamp()) ] + [ team["points"] for team in teams ]
	names.append(last)
	return {
		"points": names,
		"options": {
			"title": "YourCTF Score Progression",
			"height": 348,
			"width": "100%",
			"legend": { "position": "top" },
			"hAxis": { "textPosition": "none" },
			"vAxis": { "viewWindowMode": "explicit", "viewWindow": { "min": 0, "max": api.problem.get_max_points() } }
		}
	}

@api.cache.memoize(timeout=30000)
def get_all_team_scores(show_admin=False, show_observer=True):
	db = api.common.db_conn()
	
	teams = list(db.teams.find()) if show_admin else list(db.teams.find({ "admin": { "$ne": True } }))
	submissions = list(db.submissions.find({ "correct": True, "timestamp": { "$lt": api.config.end_time.timestamp() } }).sort("timestamp", 1))
	problems = list(db.problems.find({}))
	users = list(db.users.find({}))
	
	scoreboard = []
	
	pvalue = {}
	bpoints = {}
	for problem in problems:
		pvalue[problem["pid"]] = problem["value"]
		bpoints[problem["pid"]] = problem["bonus_points"]
	
	for i in range(len(teams)):
		team = teams[i]
		solved = []
		pts = 0
		last_updated = 0
		for submission in submissions:
			if submission["tid"] == team["tid"] and submission["pid"] not in solved:
				solved.append(submission["pid"])
				time = submission["timestamp"]
				if time > last_updated:
					last_updated = time
				value = pvalue[submission["pid"]]
				if submission["bonus_place"] != -1:
					value *= round((1.0 + bpoints[submission["pid"]][submission["bonus_place"]]), 2)
				pts += value
		teams[i]["points"] = pts
		teams[i]["last_updated"] = last_updated
		teams[i]["observer"] = False
		for user in users:
			if "team" in user and user["team"] == team["tid"] and user["type"] != 1:
				teams[i]["observer"] = True
				break
	
	def teams_sort(a, b):
		if a["points"] > b["points"]: return -1
		elif a["points"] < b["points"]: return 1
		else: return a["last_updated"] - b["last_updated"]
	teams.sort(key=api.common.cmp_to_key(teams_sort))
	
	observers = 0
	for i in range(len(teams)):
		team = teams[i]
		if team["observer"]:
			observers += 1
		team_info = {
			"rank": i + 1 - observers,
			"tid": team["tid"],
			"teamname": team["teamname"],
			"points": team["points"],
			"observer": team["observer"],
		}
		if "school" in team:
			team_info["school"] = team["school"]
		if not(show_observer == False and team["observer"]):
			scoreboard.append(team_info)
	
	return scoreboard