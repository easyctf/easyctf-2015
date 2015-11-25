import bcrypt, re, urllib, flask, requests, json
import api
import api.auth
import api.user
import api.common
import api.config
import os

def get_users():
	db = api.common.db_conn()
	
	users = list(db.users.find({ "team": { "$exists": False } }))
	result = []
	
	for user in users:
		result.append({
			"username": user["username"],
			"name": user["name"],
			"uid": user["uid"]
		})
	
	return result

# oops never finished