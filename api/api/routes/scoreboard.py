from flask import request, session
from flask import Blueprint

import api
import json
import mimetypes
import os.path
import api.auth

import asyncio
import threading

from api.annotations import api_wrapper
from api.common import flat_multi
from api.exceptions import *

blueprint = Blueprint("scoreboard_api", __name__)

# guess there's nothing here :P