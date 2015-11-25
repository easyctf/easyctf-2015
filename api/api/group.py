import api
import api.common

from voluptuous import Required, Length, Schema
from api.schemas import check, verify_to_schema
from api.exceptions import *

group_schema = Schema({
	Required("groupname"): check(
		([str, Length(min=4, max=32)], "Class name must be between 4 and 32 characters.")
	)
}, extra=True)

def is_owner_of_group(gid):
	group = get_group(gid=gid)
	if api.auth.is_logged_in():
		uid = api.user.get_user()["uid"]
	else:
		raise WebException("You're not logged in!")
	
	return uid == group["owner"]

def is_member_of_group(gid=None, name=None, owner_uid=None, tid=None):
	group = get_group(gid=gid, name=name, owner_uid=owner_uid)
	if tid is None:
		if api.auth.is_logged_in():
			tid = api.user.get_team()["tid"]
		else:
			raise WebException("You're not logged in!")
	
	return tid in group["members"]
	
def get_member_information(gid):
	group = get_group(gid=gid)
	member_information = [api.team.get_team_information(tid) for tid in group["members"]]
	return member_information

def create_group(uid, group_name):
	db = api.common.db_conn()
	gid = "grps_" + api.common.token()
	db.groups.insert({
		"name": group_name,
		"owner": uid,
		"members": [ ],
		"gid": gid
	})
	return gid

def create_group_request(params, uid=None):
	if uid is None:
		uid = api.user.get_user()["uid"]
	
	verify_to_schema(group_schema, params)
	
	if get_group(name=params["groupname"], owner_uid=uid) is not None:
		raise WebException("A class with that name already exists!")
		
	return create_group(uid, params["groupname"])

def delete_group_request(params):
	if "gid" not in params:
		raise WebException("You can't delete a class that doesn't exist!")
	
	gid = params["gid"]
	user = api.user.get_user()
	group = get_group(gid)
	
	if group["owner"] != user["uid"]:
		raise WebException("You can't delete a class that you didn't create!")
		
	db = api.common.db_conn()
	db.groups.remove({
		"gid": gid
	})
	return

def add_member(params):
	if "gid" not in params or "join_code" not in params:
		raise WebException("Please enter a join code.")
	
	gid = params["gid"]
	join_code = params["join_code"]
	group = get_group(gid)
	user = api.user.get_user()
	
	if group["owner"] != user["uid"]:
		raise WebException("You can't add teams to a class that you didn't create!")
		
	db = api.common.db_conn()
	team = db.teams.find_one({ "join_code": join_code })
	if team is None:
		raise WebException("No team was found with that join code. Maybe check with them again?")
	group = db.groups.find_one({ "gid": gid })
	if team["tid"] in group["members"]:
		raise WebException("That team's already in the group!")
	
	if team in group["members"]:
		raise WebException("You can't add a team to a group to which it already belongs!")
	
	db.groups.update_one({
		"gid": gid
	}, {
		"$push": {
			"members": team["tid"]
		}
	})
	return

def remove_member(params):
	if "gid" not in params or "tid" not in params:
		raise WebException("Please use the interface.")
	
	gid = params["gid"]
	group = get_group(gid)
	user = api.user.get_user()
	
	if group["owner"] != user["uid"]:
		raise WebException("You can't remove teams from a class that you didn't create!")
	
	db = api.common.db_conn()
	group = db.groups.find_one({ "gid": gid })
	if params["tid"] not in group["members"]:
		raise WebException("That team's not in the group!")
	
	db.groups.update_one({
		"gid": gid
	}, {
		"$pull": {
			"members": params["tid"]
		}
	})
	
def get_group(gid=None, name=None, owner_uid=None):
	db = api.common.db_conn()
	
	match = {}
	if name is not None and owner_uid is not None:
		match.update({ "name": name })
		match.update({ "owner": owner_uid })
	elif gid is not None:
		match.update({ "gid": gid })
	else:
		raise WebException("Something screwed up.")
	
	group = db.groups.find_one(match, { "_id": 0 })
	return group

# def add_team_to_group(join_code, gid):

def get_groups(uid=None):
	db = api.common.db_conn()
	
	def get_group_members(tids):
		teams = []
		for tid in tids:
			team = api.team.public_info(tid=tid)
			if team is not None:
				users = { }
				for user in list(db.users.find({ "team": tid })):
					users[user["uid"]] = {
						"uid": user["uid"],
						"name": user["name"],
						"username": user["username"]
					}
				team["members"] = users
				teams.append(team)
		return teams
	
	if uid is None:
		uid = api.user.get_user()["uid"]
	groups = []
	
	for group in list(db.groups.find({ "owner": uid }, { "name": 1, "gid": 1, "owner": 1, "members": 1 }).sort("name", 1)):
		owner = api.user.get_user(uid=group["owner"])["username"]
		groups.append({
			"name": group["name"],
			"gid": group["gid"],
			"members": get_group_members(group["members"]),
			"owner": owner
			# average score?
		})
	return groups
