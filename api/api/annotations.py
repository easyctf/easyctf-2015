import json, traceback
import api

from api.exceptions import *
from datetime import datetime
from functools import wraps
from flask import session, request, abort

def api_wrapper(f):
	@wraps(f)
	def wrapper(*args, **kwds):
		web_result = {}
		response = 200
		try:
			web_result = f(*args, **kwds)
		except WebException as error:
			response = 200
			web_result = { "success": 0, "message": str(error) }
		except APIException as error:
			response = 500
			web_result = { "success": 0, "message": str(error) }
		except Exception as error:
			response = 200
			traceback.print_exc()
			web_result = { "success": 0, "message": "Something went wrong! Please notify us about this immediately.", error: traceback.format_exc() }
		return json.dumps(web_result), response, { "Content-Type": "application/json; charset=utf-8" }
	return wrapper

def require_login(f):
	@wraps(f)
	def wrapper(*args, **kwds):
		if not api.auth.is_logged_in():
			raise WebException("You must be logged in.")
		return f(*args, **kwds)
	return wrapper

def require_teacher(f):
	@require_login
	@wraps(f)
	def wrapper(*args, **kwds):
		if not session.get("admin", False):
			if not api.user.is_teacher():
				raise WebException("You must be a teacher!")
		return f(*args, **kwds)
	return wrapper

def require_team(f):
	@require_login
	@wraps(f)
	def wrapper(*args, **kwds):
		if not session.get("admin", False):
			user = api.user.get_user()
			in_team = "team" in user and len(user["team"]) > 1
			if not in_team:
				raise WebException("You must be in a team!")
		return f(*args, **kwds)
	return wrapper
	
def check_csrf(f):
	@wraps(f)
	@require_login
	def wrapper(*args, **kwds):
		if "token" not in session:
			raise WebException("CSRF token is not in session.")
		if "token" not in request.form:
			raise WebException("CSRF token is not in form.")
		if session["token"] != request.form["token"]:
			raise WebException("The token is invalid.")
		return f(*args, **kwds)
	return wrapper

def require_admin(f):
	@wraps(f)
	def wrapper(*args, **kwds):
		if not session.get("admin", False):
			raise WebException("You must be an admin!")
		return f(*args, **kwds)
	return wrapper

def block_before_competition(return_result):
	def decorator(f):
		@wraps(f)
		def wrapper(*args, **kwds):
			# print(datetime.utcnow().timestamp())
			# print(api.config.start_time.timestamp())
			if session.get("admin", False) == True or datetime.utcnow().timestamp() > api.config.start_time.timestamp():
				return f(*args, **kwds)
			else:
				raise WebException(return_result)
		return wrapper
	return decorator

def block_after_competition(return_result):
	def decorator(f):
		@wraps(f)
		def wrapper(*args, **kwds):
			if session.get("admin", False) == True or datetime.utcnow().timestamp() < api.config.end_time.timestamp():
				return f(*args, **kwds)
			else:
				raise WebException(return_result)
		return wrapper
	return decorator