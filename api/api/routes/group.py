from flask import request, session
from flask import Blueprint

import api
import json
import mimetypes
import os.path
import api.auth

import api.cache

import api.stats

import asyncio
import threading

from api.annotations import *
from api.common import flat_multi
from api.exceptions import *

blueprint = Blueprint("group_api", __name__)

@blueprint.route("/list", methods=["GET"])
@api_wrapper
@require_login
@require_teacher
def get_group_list_hook():
	return { "success": 1, "data": api.group.get_groups() }

@blueprint.route("/create", methods=["POST"])
@api_wrapper
@require_login
@require_teacher
def create_group_hook():
	gid = api.group.create_group_request(api.common.flat_multi(request.form))
	return { "success": 1, "message": "Successfully created class! Reloading..." }

@blueprint.route("/delete", methods=["POST"])
@api_wrapper
@require_login
@require_teacher
def delete_group_hook():
	api.group.delete_group_request(api.common.flat_multi(request.form))
	return { "success": 1, "message": "Group was deleted. Reloading..." }

@blueprint.route("/add_team", methods=["POST"])
@api_wrapper
@require_login
@require_teacher
def add_team_group_hook():
	api.group.add_member(api.common.flat_multi(request.form))
	return { "success": 1, "message": "Successfully added team! Reloading..." }

@blueprint.route("/remove_team", methods=["POST"])
@api_wrapper
@require_login
@require_teacher
def remove_team_group_hook():
	api.group.remove_member(api.common.flat_multi(request.form))
	return { "success": 1, "message": "Successfully removed team! Reloading..." }