import bcrypt, re, urllib, flask, requests
import api
import api.auth
import api.user
import api.common
import api.config

from datetime import datetime

from voluptuous import Schema, Length, Required
from api.schemas import verify_to_schema, check
from api.exceptions import *
from flask import request

__check_ascii = lambda s: all(ord(c) < 128 for c in s)
__check_teamname = lambda teamname: get_team(teamname=teamname) is None

TeamSchema = Schema({
	Required("teamname"): check(
		([str, Length(min=3, max=32)], "Your teamname should be between 3 and 32 characters long."),
		([__check_ascii], "Please only use ASCII characters in your teamname."),
		([__check_teamname], "This teamname is taken.")
	),
	"school": str
}, extra=True)

max_team_users = 5

""" /api/team/create """

def create(params):
	db = api.common.db_conn()
	teamname = params["teamname"]
	if len(teamname) > 32:
		raise WebException("Team name too long!")
	params["school"] = ""
	verify_to_schema(TeamSchema, params)
	user = api.user.get_user()
	if api.user.in_team():
		raise WebException("You can't create a team if you're already in one!")
	tid = "team_" + api.common.token()
	team = {
		"tid": tid,
		"teamname": teamname,
		"last_updated": int(datetime.now().timestamp()),
		"owner": user['uid']
	}
	db.teams.insert(team)
	db.users.update_one({ "uid": user['uid'] }, {
		"$set": {
			"team": tid
		}
	})
	return tid

def members():
	if api.user.in_team():
		db = api.common.db_conn()
		team = get_team()
		members_raw = list(db.users.find({ "team": team['tid'] }))
		members = []
		for member in members_raw:
			members.append({
				"uid": member['uid'],
				"email": member['email'],
				"name": member['name']
			})
		return members
	else:
		raise WebException("You must be in a team to see your teammates!")

def join(code):
	if not api.user.in_team():
		db = api.common.db_conn()
		team = db.teams.find_one({ "join_code": code })
		uid = api.auth.get_uid()
		if team is not None:
			members = list(db.users.find({ "team": team["tid"] }))
			if len(members) < api.config.max_players or ("admin" in team and team["admin"] == True):
				db.users.update({ "uid": uid }, { "$set": { "team": team["tid"] } })
				if "admin" in team and team["admin"] == True:
					db.users.update_many({ "team": team["tid"] }, { "$set": { "type": 0 } })
				return "Successfully joined this team!"
			else:
				raise WebException("There's already " + str(api.config.max_players) + " members in that team!")
		else:
			raise WebException("That team was not found.")
	else:
		raise WebException("You can't join a team if you're already in one!")

def join_code(force=False):
	if api.user.in_team():
		db = api.common.db_conn()
		team = get_team()
		user = api.user.get_user()
		teamowner = user["uid"] == team["owner"]
		if teamowner:
			if force:
				return generate_join_code()
			else:
				if "join_code" in team:
					return team["join_code"]
				else:
					return generate_join_code()
		else:
			raise WebException("You must be the owner of a team to get the join code!")
	else:
		raise WebException("You must be in a team to get the join code!")

def remove(uid):
	if api.user.in_team():
		user = api.user.get_user()
		team = get_team()
		db = api.common.db_conn()
		teamowner = user["uid"] == team["owner"]
		if uid == user["uid"]:
			if teamowner:
				db.users.update_many({ "team": user["team"] }, { "$unset": { "team": 1 } })
				db.teams.delete_one({ "tid": user["team"] })
				return "Successfully disbanded the team."
			else:
				db.users.update_one({ "uid": user["uid"] }, { "$unset": { "team": 1 } })
				return "Successfully left your team."
		else:
			if teamowner:
				db.users.update_one({ "uid": uid }, { "$unset": { "team": 1 } })
				return "Successfully removed this member."
			else:
				# fuck you
				raise WebException("You must be owner to remove other members.")
	else:
		raise WebException("You must be in a team to remove someone!")

def update(attrs):
	if api.user.in_team():
		db = api.common.db_conn()
		team = get_team()
		user = api.user.get_user()
		teamowner = user["uid"] == team["owner"]
		if teamowner:
			team_info = {
				"teamname": team["teamname"]
			}
			if "school" in team: team_info["school"] = team["school"]
			if team_info == attrs: return False
			if "teamname" in attrs: team_info["teamname"] = attrs["teamname"]
			if "school" in attrs: team_info["school"] = attrs["school"]
			xteam = get_team(teamname=attrs["teamname"])
			if xteam is not None and xteam["tid"] != team["tid"]: raise WebException("There's already another team with that name!")
			teamname = attrs["teamname"]
			if len(teamname) > 32:
				raise WebException("Team name too long!")
			team_info["teamname"] = teamname
			school = attrs["school"]
			if len(teamname) > 64:
				raise WebException("School too long!")
			team_info["school"] = school
			db.teams.update_one({ "tid": team["tid"] }, {
				"$set": team_info
			})
			return True
		else:
			raise WebException("You must be the owner of a team to update team info!")
	else:
		raise WebException("You must be in a team to update team info!")
		
@api.cache.memoize(timeout=120)
def public_info(teamname=None, tid=None):
	db = api.common.db_conn()
	team = get_team(teamname=teamname, tid=tid)
	if team is None:
		return None
	
	s = db.submissions.find({ "tid": team["tid"] })
	submissions = list(s) if s is not None else []
	problems = list(db.problems.find({}))
	
	submission_successes = 0
	submission_failures = 0
	categories = {}
	solved = []
	solved_pids = []
	for submission in submissions:
		if submission["correct"] == True:
			submission_successes += 1
			if submission["category"] in categories:
				categories[submission["category"]] += 1
			else:
				categories[submission["category"]] = 1
			solved.append({
				"pid": submission["pid"],
				"category": submission["category"],
				"timestamp": submission["timestamp"],
				"bonus_place": submission["bonus_place"],
				"by": submission["uid"],
				"solved": True
			})
			solved_pids.append(submission["pid"])
		else:
			submission_failures += 1
	category_breakdown = { }
	cardinal = [ "1st", "2nd", "3rd" ]
	points = 0
	for problem in problems:
		for i in range(len(solved)):
			if solved[i]["pid"] == problem["pid"]:
				if problem["category"] not in category_breakdown:
					category_breakdown[problem["category"]] = [ ]
				solved[i]["problem"] = problem["title"]
				value = problem["value"]
				if solved[i]["bonus_place"] != -1:
					value *= (1.0 + problem["bonus_points"][solved[i]["bonus_place"]])
				solved[i]["points"] = value
				points += value
				category_breakdown[problem["category"]].append(solved[i])
				break
	for problem in problems:
		if problem["category"] not in category_breakdown.keys():
			category_breakdown[problem["category"]] = [ ]
		if problem["pid"] not in solved_pids:
			category_breakdown[problem["category"]].append({
				"solved": False
			})
	solved.sort(key=lambda x: x["timestamp"], reverse=True)
	
	members = list(db.users.find({ "team": team["tid"] }))
	team_members = [ ]
	for member in members:
		team_members.append({
			"name": member["name"],
			"username": member["username"]
		})
	
	result = {
		"tid": team["tid"],
		"teamname": team["teamname"],
		"members": team_members,
		# "submission_successes": submission_successes,
		# "submission_failures": submission_failures,
		# "category_breakdown": category_breakdown,
		"score": points,
		"score_progression": api.stats.get_team_score_progression(tid=team["tid"])
	}
	
	if "school" in team:
		result["school"] = team["school"]
	
	scoreboard = api.stats.get_all_team_scores()
	for team2 in scoreboard:
		if team2["tid"] == team["tid"]:
			result["rank"] = team2["rank"]
			break
	
	if datetime.utcnow().timestamp() > api.config.start_time.timestamp():
		result["submission_successes"] = submission_successes
		result["submission_failures"] = submission_failures
		result["category_breakdown"] = category_breakdown
	return result

def get_schools():
	db = api.common.db_conn()
	schools = []
	schools_lowercase = []
	teams = list(db.teams.find({}))
	for team in teams:
		if "school" in team and not(team["school"].lower() in schools_lowercase):
			schools_lowercase.append(team["school"].lower())
			schools.append(team["school"])
	return schools
	
def assign_shell_account(tid):
	if tid is None:
		raise WebException("You must be logged in.")
	if not api.user.in_team():
		raise WebException("You must be in a team.")
	team = api.team.get_team()
	if "admin" in team and team["admin"] == True:
		pass
	else:
		now = datetime.now().timestamp()
		if now < api.config.start_time.timestamp():
			raise WebException("Contest hasn't started yet.")
		else:
			pass
	db = api.common.db_conn()
	shell_account = db.shell_accounts.find_one({
		"assigned": { "$ne": True }
	})
	db.teams.update_one({ "tid": tid }, {
		"$set": { "shell_user": shell_account["username"], "shell_pass": shell_account["password"] }
	})
	db.shell_accounts.update_one({ "username": shell_account["username"] }, {
		"$set": { "assigned": True, "tid": tid }
	})
	return shell_account
	
def get_team_members(tid=None, name=None):
	db = api.common.db_conn()
	tid = get_team(teamname=name, tid=tid)["tid"]
	
	users = list(db.users.find({ "tid": tid },
		{ "_id": 0, "uid": 1, "username": 1 }))
	return users

def get_team_uids(tid=None, name=None):
	return [user["uid"] for user in get_team_members(tid=tid, name=name)]
	
def get_team_information(tid=None):
	team_info = get_team(tid=tid)
	
	if tid is None:
		tid = team_info["tid"]
	
	team_info["score"] = api.stats.get_score(tid=tid)
	team_info["members"] = [member["username"] for member in get_team_members(tid=tid)]
	team_info["max_team_size"] = max_team_users
	
	return team_info

def get_all_teams(observer=False):
	match = {}
	
	db = api.common.db_conn()
	return list(db.teams.find(match, { "_id": 0 }))

def get_groups(tid=None, uid=None):
	db = api.common.db_conn()
	
	def get_group_members(tids):
		teams = []
		for tid in tids:
			team = public_info(tid=tid)
			if team is not None:
				teams.append({
					"tid": team["tid"],
					"teamname": team["teamname"]
				})
		return teams
	
	tid = get_team(tid=tid)["tid"]
	groups = []
	
	for group in list(db.groups.find({ "members": tid }, { "name": 1, "gid": 1, "owner": 1, "members": 1 }).sort("name", 1)):
		owner = api.user.get_user(uid=group["owner"])["username"]
		groups.append({
			"name": group["name"],
			"gid": group["gid"],
			"members": get_group_members(group["members"]),
			"owner": owner
		})
	return groups
	
""" Helper functions """

def get_team(teamname=None, tid=None):
	db = api.common.db_conn()
	match = {}
	if teamname != None:
		match.update({ "teamname": teamname })
	elif tid != None:
		match.update({ "tid": tid })
	elif api.auth.is_logged_in() and api.user.in_team():
		match.update({ "tid": api.user.get_user()['team'] })
	# else:
		# return None
	result = db.teams.find_one(match)
	return result

def generate_join_code():
	code = "tmjn_" + api.common.token()
	db = api.common.db_conn()
	user = api.user.get_user()
	db.teams.update_one({ "tid": user["team"] }, {
		"$set": { "join_code": code }
	})
	return code

def is_observer_team(tid=None):
	if tid is None:
		return False
	
	db = api.common.db_conn()
	users = list(db.users.find({ "team": tid }))
	
	observer = False
	for user in users:
		if user["type"] > 1:
			observer = True
			break
	
	return observer

def is_admin_team(tid=None):
	if tid is None:
		return False
	
	team = get_team(tid=tid)
	return "admin" in team and team["admin"] == True