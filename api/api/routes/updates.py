from flask import Blueprint
from flask import request

import api

from api.annotations import *
from api.common import flat_multi
from api.exceptions import *

blueprint = Blueprint("updates_api", __name__)

@blueprint.route("/get", methods=["GET"])
@api_wrapper
def updates_get_hook():
	updates = api.updates.get_all()
	user = None
	if api.auth.is_logged_in(): user = api.user.get_user()
	data = []
	for update in updates:
		u = {
			"title": update["title"],
			"timestamp": update["timestamp"],
			"content": update["content"],
			"author": update["author"],
			"upid": update["upid"]
		}
		data.append(u)
	return { "success": 1, "data": data, "can_deactivate": user is not None and user["type"] == 0 }

@blueprint.route("/post", methods=["POST"])
@api_wrapper
@require_login
@require_admin
def updates_post_hook():
	data = api.common.flat_multi(request.form)
	api.updates.post_update(data)
	return { "success": 1, "message": "Posted!" }

@blueprint.route("/remove", methods=["POST"])
@api_wrapper
@require_login
@require_admin
def updates_deactivate_hook():
	upid = request.form.get("upid")
	if upid is not None:
		api.updates.deactivate(upid)
		return { "success": 1, "message": "Removed!" }
	else:
		raise WebException("stop doing stupid things")