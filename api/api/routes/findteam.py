from flask import request, session
from flask import Blueprint

import api
import json
import mimetypes
import os.path
import api.auth

import asyncio
import threading

from api.annotations import api_wrapper, require_login
from api.common import flat_multi
from api.exceptions import *

blueprint = Blueprint("findteam_api", __name__)

@blueprint.route("/list_users", methods=["GET"])
@api_wrapper
@require_login
def get_user_list_hook():
	return { "success": 1, "data": api.findteam.get_users() }

@blueprint.route("/send_invite", methods=["POST"])
@api_wrapper
@require_login
def post_invite_hook():
	return { "success": 0 }
	return { "success": 1, "data": api.findteam.get_users() }