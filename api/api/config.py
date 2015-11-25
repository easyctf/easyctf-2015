import api
import api.app

import datetime
import moment

api.app.session_cookie_domain = "www.yourctf.com" # the domain you're on
api.app.session_cookie_path = "/"
api.app.session_cookie_name = "flask"

api.app.secret_key = "" # secret key for flask cookies

api.common.allowed_protocols = [ "https", "http" ]
api.common.allowed_ports = [ 8080 ]

# local mongo server
api.common.mongo_db_name = "yourctf"
api.common.mongo_addr = "127.0.0.1"
api.common.mongo_port = 27017

# please customize the following
competition_name = "CTF"
max_players = 5
http_dir = "/srv/http/ctf"
basedir = "/home/user/yourctf" # this is the root folder of the platform (that contains deploy, deploy_api, etc.)

recaptcha_secret = "" # secret (server) key from recaptcha

class EST(datetime.tzinfo):
	def __init__(self, utc_offset):
		self.utc_offset = utc_offset
	def utcoffset(self, dt):
		return datetime.timedelta(hours=-self.utc_offset)
	def dst(self, dt):
		return datetime.timedelta(0)

# please customize the dates
start_time = datetime.datetime(2015, 11, 3, 20, 0, 0, tzinfo=EST(6))
end_time = datetime.datetime(2015, 11, 11, 20, 0, 0, tzinfo=EST(6))

mailchimp_secret = "" # mailchimp secret
mailchimp_subscriber_list = "" # list if you want to subscribe people

sendgrid_apikey = "" # sendgrid (for forgot password and such)

# not actually used so doesn't matter
shell = {
	"host": "www.yourctf.com",
	"port": 22,
	"privatekey_file": "~/.ssh/id_rsa"
}