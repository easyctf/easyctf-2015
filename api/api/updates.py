import api

from api.common import token
from api.exceptions import *
from datetime import datetime

def get_all():
	db = api.common.db_conn()
	updates = list(db.updates.find({ "active": True }).sort("timestamp", -1))
	return updates

def post_update(params):
	user = api.user.get_user()
	params["author"] = user["name"]
	params["timestamp"] = datetime.utcnow().timestamp()
	params["active"] = True
	params["upid"] = "updt_" + api.common.token()
	
	db = api.common.db_conn()
	db.updates.insert(params)
	return

def deactivate(upid):
	db = api.common.db_conn()
	db.updates.update_one({ "upid": upid }, {
		"$set": { "active": False }
	})
	return