from functools import wraps
from bson import json_util, datetime

import time
import api
# import timestamp
from api.exceptions import *

no_cache = False
fast_cache = {}
_mongo_index = None

def clear_all():
	db = api.common.db_conn()
	db.cache.remove()
	fast_cache.clear()

def get_mongo_key(f, *args, **kwargs):
	min_kwargs = dict(filter(lambda pair: pair[1] is not None, kwargs.items()))
	return {
		"function": "{}.{}".format(f.__module__, f.__name__),
		"args": args,
		"kwargs": min_kwargs
	}

def get_key(f, *args, **kwargs):
	if len(args) > 0:
		kwargs["#args"] = ",".join(map(str, args))
	
	sorted_keys = sorted(kwargs)
	arg_key = "&".join(["{}:{}".format(key, kwargs[key]) for key in sorted_keys])
	
	key = "{}.{}${}".format(f.__module__, f.__name__, arg_key).replace(" ", "~")
	return key

def get(key, fast=False):
	if fast:
		return fast_cache.get(key, None)
	
	db = api.common.db_conn()
	cached_result = db.cache.find_one(key)
	
	if cached_result is None:
		return None
	
	if int(time.time()) > cached_result["expireAt"].timestamp():
		return None
	
	if cached_result:
		return cached_result["value"]
	# raise WebException("Something screwed up.")

def set(key, value, timeout=120, fast=False):
	if fast:
		fast_cache[key] = {
			"result": value,
			"timeout": timeout,
			"set_time": time.time()
		}
		return
	
	db = api.common.db_conn()
	update = key.copy()
	update.update({ "value": value })
	
	if timeout is not None:
		expireAt = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
		update.update({ "expireAt": expireAt })
	
	db.cache.update(key, update, upsert=True)

def timed_out(info):
	return int(time.time()) - info["set_time"] > info["timeout"]

def memoize(timeout=120, fast=False):
	assert(not fast or (fast and timeout is not None)), "You can't set fast cache without a timeout!"
	
	def decorator(f):
		@wraps(f)
		def wrapper(*args, **kwargs):
			if not kwargs.get("cache", True):
				kwargs.pop("cache", None)
				return f(*args, **kwargs)
			
			key = get_key(f, *args **kwargs) if fast else get_mongo_key(f, *args, **kwargs)
			cached_result = get(key, fast=fast)
			
			if cached_result is None or no_cache or (fast and timed_out(cached_result)):
				function_result = f(*args, **kwargs)
				set(key, function_result, timeout=timeout, fast=fast)
				return function_result
			
			return cached_result["result"] if fast else cached_result
		return wrapper
	return decorator

def invalid_memoization(f, args):
	db = api.common.db_conn()
	
	search = { "function": "{}.{}".format(f.__module__, f.__name__) }
	search["args"] = list(args)
	print(search)
	# search.update({ "$or": list(keys) })
	
	db.cache.remove(search)