from flask import request, session
from flask import Blueprint

import api
import json
import mimetypes
import os.path
import api.auth

import asyncio
import threading

from api.annotations import *
from api.common import flat_multi
from api.exceptions import *

blueprint = Blueprint("password_recovery_api", __name__)

@blueprint.route("/forgot", methods=["POST"])
@api_wrapper
def forgot_hook():
	params = api.common.flat_multi(request.form)
	params["ip"] = request.remote_addr
	api.password_recovery.send_email(params)
	return { "success": 1, "message": "Email was sent! Go check your inbox (and your spam box. and your other boxes)" }

@blueprint.route("/reset", methods=["POST"])
@api_wrapper
def reset_hook():
	params = api.common.flat_multi(request.form)
	api.password_recovery.reset_password(params)
	return { "success": 1, "message": "Recovery successful. Don't lose it again!" }