from flask import Flask, send_file, render_template, request, session
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__, static_path="/")
app.wsgi_app = ProxyFix(app.wsgi_app)

import api
import json
import mimetypes
import os.path
import random
import logging
import sys
import requests

from datetime import datetime

import api.routes.findteam
import api.routes.group
import api.routes.password_recovery
import api.routes.problem
import api.routes.programming
import api.routes.scoreboard
import api.routes.stats
import api.routes.team
import api.routes.updates
import api.routes.user
from api.annotations import api_wrapper

session_cookie_domain = "127.0.0.1"
session_cookie_path = "/"
session_cookie_name = "flask"

secret_key = ""

def config_app(*args, **kwargs):
	app.secret_key = secret_key
	app.config["SESSION_COOKIE_DOMAIN"] = session_cookie_domain
	app.config["SESSION_COOKIE_PATH"] = session_cookie_path
	app.config["SESSION_COOKIE_NAME"] = session_cookie_name
	
	app.config["MAX_CONTENT_LENGTH"] = 128 * 1024
	app.config["DEBUG"] = True

	app.register_blueprint(api.routes.findteam.blueprint, url_prefix="/api/findteam")
	app.register_blueprint(api.routes.group.blueprint, url_prefix="/api/group")
	app.register_blueprint(api.routes.password_recovery.blueprint, url_prefix="/api/password_recovery")
	app.register_blueprint(api.routes.problem.blueprint, url_prefix="/api/problem")
	app.register_blueprint(api.routes.programming.blueprint, url_prefix="/api/programming")
	app.register_blueprint(api.routes.scoreboard.blueprint, url_prefix="/api/scoreboard")
	app.register_blueprint(api.routes.stats.blueprint, url_prefix="/api/stats")
	app.register_blueprint(api.routes.team.blueprint, url_prefix="/api/team")
	app.register_blueprint(api.routes.updates.blueprint, url_prefix="/api/updates")
	app.register_blueprint(api.routes.user.blueprint, url_prefix="/api/user")
	
	app.logger.addHandler(logging.StreamHandler(sys.stdout))
	app.logger.setLevel(logging.DEBUG)
	
	app.logger.debug("Starting CTF API...")
	
	# api.logger.setup_logs({ "verbose": 2 })
	return app

@app.after_request
def after_request(response):
	response.headers.add("Access-Control-Allow-Methods", "GET, POST")
	response.headers.add("Access-Control-Allow-Credentials", "true")
	response.headers.add("Access-Control-Allow-Headers", "Content-Type, *")
	response.headers.add("Cache-Control", "no-cache")
	response.headers.add("Cache-Control", "no-store")
	
	if api.auth.is_logged_in():
		if "token" in session:
			response.set_cookie("token", session["token"])
		else:
			csrf_token = "csrf_" + api.common.token()
			session["token"] = csrf_token
			response.set_cookie("token", csrf_token)
	
	return response

@app.route("/api/time", methods=["GET"])
@api_wrapper
def get_time():
	return { "success": 1, "data": { "time": int(datetime.utcnow().timestamp()) } }

@app.route("/api/dank_memes", methods=["GET"])
@api_wrapper
def get_memes():
	return { "Easter Egg Hunt": "egg{i_like_my_memes_nice_and_fresh}" }

@app.route("/api/our_team", methods=["GET"])
@api_wrapper
def get_team():
	r = requests.get("https://slack.com/api/users.list", params={ "token": "xxxxxxxxxxxxxxxxx" })
	data = json.loads(r.text)
	members = [ ]
	for member in data["members"]:
		if member["deleted"] == False:
			members.append({
				"name": member["profile"]["real_name_normalized"],
				"picture": member["profile"]["image_192"],
				"what_i_do": member["profile"]["title"] if ("title" in member["profile"] and len(member["profile"]["title"]) > 0) else "&nbsp;"
			})
	return { "success": 1, "team": members }
