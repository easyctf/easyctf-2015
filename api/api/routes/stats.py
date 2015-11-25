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

from api.annotations import api_wrapper
from api.common import flat_multi
from api.exceptions import *

blueprint = Blueprint("stats_api", __name__)

@blueprint.route("/scoregraph", methods=["GET"])
@api_wrapper
def stats_scoregraph_hook():
	result = api.stats.get_scoregraph()
	return { "success": 1, "data": result }

@blueprint.route("/scoreboard", methods=["GET"])
@api_wrapper
def stats_scoreboard_hook():
	result = {}
	result["scores"] = api.stats.get_all_team_scores()
	
	if api.auth.is_logged_in() and api.user.in_team():
		for i in range(len(result["scores"])):
			if result["scores"][i]["tid"] == api.user.get_user()["team"]:
				result["scores"][i]["my_team"] = True
				break
	
	if api.auth.is_logged_in() and api.user.in_team():
		team = api.team.get_team()
		groups = api.team.get_groups(tid=team["tid"])
		result["groups"] = groups
		
	return { "success": 1, "data": result }

@blueprint.route("/scoreboard/all", methods=["GET"])
@api_wrapper
def stats_scoreboard_all_hook():
	result = {}
	result = api.stats.get_all_team_scores(show_admin=True)
	return { "success": 1, "data": result }

@blueprint.route("/score_progression/<tid>", methods=["GET"])
@api_wrapper
def stats_score_progression_hook(tid):
	return { "success": 1, "data": api.stats.get_team_score_progression(tid=tid) }