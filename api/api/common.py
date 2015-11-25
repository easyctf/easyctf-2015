import json
import uuid
import html
import os
import traceback

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, InvalidName
from voluptuous import Invalid, MultipleInvalid
from functools import wraps

from api.exceptions import *

mongo_addr = "127.0.0.1"
mongo_port = 27017
mongo_db_name = ""
mongo_db_user = os.environ.get("DB_USER")
mongo_db_pass = os.environ.get("DB_PASS")

__connection = None
__client = None
external_client = None

def escape(text):
	return html.escape(text)

def db_conn():
    if external_client is not None:
        return external_client

    global __client, __connection
    if not __connection:
        try:
            __client = MongoClient(mongo_addr, mongo_port)
            __connection = __client[mongo_db_name]
        except ConnectionFailure:
            raise Exception("Could not connect to mongo database {} at {}:{}".format(mongo_db_name, mongo_addr, mongo_port))
        except InvalidName as error:
            raise Exception("Database {} is invalid! - {}".format(mongo_db_name, error))

    return __connection
	
def flat_multi(multidict):
	flat = {}
	for key, values in multidict.items():
		flat[key] = values[0] if type(values) == list and len(values) == 1 \
					else values
	return flat

def token():
	return str(uuid.uuid4().hex)

def cmp_to_key(mycmp):
	class K:
		def __init__(self, obj, *args):
			self.obj = obj
		def __lt__(self, other):
			return mycmp(self.obj, other.obj) < 0
		def __gt__(self, other):
			return mycmp(self.obj, other.obj) > 0
		def __eq__(self, other):
			return mycmp(self.obj, other.obj) == 0
		def __le__(self, other):
			return mycmp(self.obj, other.obj) <= 0
		def __ge__(self, other):
			return mycmp(self.obj, other.obj) >= 0
		def __ne__(self, other):
			return mycmp(self.obj, other.obj) != 0
	return K