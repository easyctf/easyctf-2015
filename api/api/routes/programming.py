from flask import request, session
from flask import Blueprint
from werkzeug import secure_filename

import api
import json
import mimetypes
import os
import os.path
import api.auth

import asyncio
import threading
import time

from datetime import datetime

from api.annotations import *
from api.common import flat_multi, token
from api.exceptions import *

blueprint = Blueprint("programming_api", __name__)

extensions = {
	"c": "c",
	"java": "java",
	"python2": "py",
	"python3": "py"
}
program_base_path = "/programs"

@blueprint.route("/upload", methods=["POST"])
@api_wrapper
@require_login
@require_team
@block_before_competition("You can't solve problems before the competition starts!")
def programming_upload_hook():
	db = api.common.db_conn()
	team = api.team.get_team()
	user = api.user.get_user()
	pid = request.form.get("pid")
	
	if not("file" in request.files):
		raise WebException("Please upload exactly 1 file!")
	file = request.files["file"]
	# print(file.filename)
	filename = secure_filename(file.filename)
	# print(filename)
	language = request.form.get("language")
	token = "prog_" + api.common.token()
	program = file.read()
	
	ticket = {
		"uid": user["uid"],
		"tid": team["tid"],
		"pid": pid,
		"token": token,
		"timestamp": datetime.now().timestamp(),
		"language": language,
		"program": program.decode('utf-8'),
		"done": False,
		"claimed": 0
	}
	db.programs.insert_one(ticket)
	
	#threading.Thread(target=api.programming.run_program, args=(token, language)).start()
	return { "success": 1, "message": "Started execution!" }

@blueprint.route("/run_code", methods=["POST"])
@api_wrapper
@require_login
@require_team
@block_before_competition("You can't solve problems before the competition starts!")
def programming_run_code_hook():
	db = api.common.db_conn()
	user = api.user.get_user()
	team = api.team.get_team()
	pid = request.form.get("pid")
	program = request.form.get("program")
	if program is None or len(program) < 1:
		raise WebException("Please submit a program!")
		
	language = request.form.get("language")
	token = "prog_" + api.common.token()
	
	ticket = {
		"uid": user["uid"],
		"tid": team["tid"],
		"pid": pid,
		"token": token,
		"timestamp": datetime.now().timestamp(),
		"language": language,
		"program": program,
		"done": False,
		"claimed": 0
	}
	db.programs.insert_one(ticket)
	
	# threading.Thread(target=api.programming.run_program, args=(token, language)).start()
	return { "success": 1, "message": "Started execution! Check below for results." }
	
@blueprint.route("/all", methods=["GET"])
@api_wrapper
@require_login
@require_team
@block_before_competition("You can't view problems before the competition starts!")
def programming_all_hook():
	db = api.common.db_conn()
	team = api.team.get_team()
	results = list(db.programs.find({
		"tid": team["tid"]
	}, projection={
		"_id": False,
		"program": False
	}).sort([("done", 1), ("timestamp", -1)]))
	return { "success": 1, "data": results }

@blueprint.route("/stdout", methods=["GET"])
@api_wrapper
@require_login
@require_team
@block_before_competition("You can't view problems before the competition starts!")
def programming_stdout_hook():
	if request.args.get("token") is None or len(request.args.get("token")) < 1:
		raise WebException("Please provide a token.")
	token = request.args.get("token")
	
	db = api.common.db_conn()
	program = db.programs.find_one({ "token": token })
	if program is None:
		raise WebException("Could not find program.")
	if "log" not in program:
		raise WebException("Could not find log.")
	return { "success": 1, "pid": program["pid"], "timestamp": program["timestamp"], "data": program["log"] }
	
@blueprint.route("/delete_run", methods=["POST"])
@api_wrapper
@require_login
@require_team
@block_before_competition("You can't view problems before the competition starts!")
def programming_delete_run_hook():
	if request.form.get("p_token") is None or len(request.form.get("p_token")) < 1:
		raise WebException("Please provide a token.")
	token = request.form.get("p_token")
	
	db = api.common.db_conn()
	program = db.programs.find_one({ "token": token })
	user = api.user.get_user()
	if "team" in user.keys() and user["team"] != program["tid"]:
		raise WebException("You can't delete someone else's program!")
	
	db.programs.remove({ "token": token })
	return { "success": 1, "message": "Deleted!" }
