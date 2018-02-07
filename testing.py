import praw

#Make your own profile file with all these variables for oauth 2
from PSBProfile import APP_UA
from PSBProfile import app_id
from PSBProfile import app_secret
from PSBProfile import app_uri
from PSBProfile import app_scopes
from PSBProfile import app_account_code
from PSBProfile import APP_REFRESH

r = praw.Reddit(APP_UA)

def login():
    print("Logging into reddit")
    r.set_oauth_app_info(app_id, app_secret, app_uri)
    r.refresh_access_information(APP_REFRESH)
    print("Log in successful")
    return r

def test():
	post = r.submit("holdthemoan", "Quick Flash Goodbye [GIF]", url="https://gfycat.com/WholeRepentantFowl")
	r.set_flair("holdthemoan", post, flair_text='flash', flair_css_class='flash')

login()
test()