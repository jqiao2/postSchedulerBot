import praw

#Make your own profile file with all these variables for oauth 2
from profile import APP_UA
from profile import app_id
from profile import app_secret
from profile import app_uri
from profile import app_scopes
from profile import app_account_code
from profile import APP_REFRESH

r = praw.Reddit(APP_UA)

def login():
    print("Logging into reddit")
    r.set_oauth_app_info(app_id, app_secret, app_uri)
    r.refresh_access_information(APP_REFRESH)
    print("Log in successful")
    return r

#login()

def test():
	for x in xrange(0,7):
		print(x)

test()
