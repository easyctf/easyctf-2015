import api

from argparse import ArgumentParser
from api.app import app

def object_from_args(args):
	return dict(args._get_kwargs()), args._get_args()

parser = ArgumentParser(description="EasyCTF API Configuration")

parser.add_argument("-v", "--verbose", action="count", help="Increase verbosity.", default=0)
parser.add_argument("-p", "--port", action="store", help="Port that server should listen on.", default=8000)
parser.add_argument("-l", "--listen", action="store", help="Host that server should listen on.", default="0.0.0.0")
parser.add_argument("-d", "--debug", action="store_true", help="Run the server in debug mode.", default=False)

args = parser.parse_args()
keyword_args, _ = object_from_args(args)

ctf = api.app.config_app()