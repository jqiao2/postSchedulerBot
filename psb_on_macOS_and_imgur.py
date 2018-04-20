import datetime
import re
import time
from pathlib import Path
from random import randint

import praw
from biplist import readPlistFromString
from imgurpython import ImgurClient
from prawcore import PrawcoreException
from xattr import xattr

from PSBProfile import FILE_PATH
from PSBProfile import IMGUR_ACCESS_TOKEN
from PSBProfile import IMGUR_CLIENT_ID
from PSBProfile import IMGUR_CLIENT_SECRET
from PSBProfile import IMGUR_REFRESH_TOKEN
from PSBProfile import REDDIT_CLIENT_ID
from PSBProfile import REDDIT_CLIENT_SECRET
from PSBProfile import REDDIT_PASSWORD
from PSBProfile import REDDIT_USERAGENT
from PSBProfile import REDDIT_USERNAME

START_POST_HOUR = 12  # default: 4
START_POST_MINUTE = 15  # default: 15
POST_DELAY = 15  # default: 15

imgur_client = ImgurClient(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET, IMGUR_ACCESS_TOKEN,
                           IMGUR_REFRESH_TOKEN)
reddit_client = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET,
                            password=REDDIT_PASSWORD, user_agent=REDDIT_USERAGENT,
                            username=REDDIT_USERNAME)


def get_subreddits(path):
    print("Processing", path[60:])
    subreddits = readPlistFromString(xattr(path).get('com.apple.metadata:_kMDItemUserTags'))
    subreddits_clean = []
    for subreddit in subreddits:
        subreddit_clean = re.compile('[^a-zA-Z2-9_]+').sub('', subreddit)
        subreddits_clean.append(subreddit_clean)
        print("/r/" + subreddit_clean)
    return subreddits_clean


def upload_image(path):
    image = imgur_client.upload_from_path(path, anon=False)
    return image['link']


def post_image(path, imgur_url, subreddit):
    try:
        # default: path[60:-4], change 60 depending on file path
        post = reddit_client.subreddit(subreddit).submit(title=path[60:-4], url=imgur_url)
        print("Posted %s (%s) to /r/%s" % (imgur_url, path[60:-4], subreddit))
    except PrawcoreException:
        print("Unable to post %s (%s) to /r/%s" % (imgur_url, path[60:-4], subreddit))


for day in range(7):
    current_time = datetime.datetime.today()
    rand_minute = START_POST_MINUTE + randint(0, 5) + randint(0, 5)
    rand_minute = 48
    start_post_time = datetime.datetime(current_time.year, current_time.month, current_time.day,
                                        START_POST_HOUR, rand_minute)
    if START_POST_HOUR <= current_time.hour and rand_minute <= current_time.minute:
        start_post_time += datetime.timedelta(days=1)
    print("Wait until %s" % (str(start_post_time)))
    time.sleep((start_post_time - current_time).seconds)

    print('starting day', day)
    path_list = Path(FILE_PATH + str(day)).glob('*.*g')
    for preprocessed_path in path_list:
        path = str(preprocessed_path)
        subreddits = get_subreddits(path)
        imgur_url = upload_image(path)
        for subreddit in subreddits:
            post_image(path, imgur_url, subreddit)

        # Time delay
        time.sleep(POST_DELAY)

    print()
