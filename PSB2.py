import praw
import time
import datetime
import sys

# This script will post onto Reddit everyday by week under some circumstances:
# 1. If you have enough karma from the subreddit to not get auto-blocked,
#    if you are, your posts won't get posted.
# 2. You put them in right, obviously.
# You will need eight seperate files for this script to work. One is the
# profile file. This includes all the APP_UA, app_id, etc to associate this
# script with your Reddit account. The other seven files are the ones that
# contain your posts for that day (i.e. file 0 contains the posts for day one,
# file 1 contains the posts for day two, all the way to file 6). There is a
# specific format these files are to be written in. which is:
# 1. Post URL
# 2. Post title
# 3. Subreddit(s) to post to
# Continue for all posts
# If a subreddit requires you to flair a post, put the flair name after the
# subreddit name, but also make sure you indicate so down below so the script
# knows to look for a flair after the subreddit name. This only works if you
# are a mod of that subreddit.


# Make your own profile file with all these variables for oauth 2
from PSBProfile import APP_UA
from PSBProfile import app_id
from PSBProfile import app_secret
from PSBProfile import app_uri
from PSBProfile import app_scopes
from PSBProfile import app_account_code
from PSBProfile import APP_REFRESH

from random import randint

# Reddit instance
r =                 praw.Reddit(APP_UA)
# Array of posts that have to get tagged NSFW
NSFWPOSTTITLES = 	[]
# Name of subreddit(s) that have flairs
FLAIRSUBS = 		"holdthemoan"
# Hour time to post (24 hour time)
TIMEHOUR =          4
# Minute time to post minus five
TIMEMINUTE =        30
# Seconds between each post
POSTDELAY =         30

def login():
    print("Logging into reddit")
    hello = True
    while hello:
        try:
            r.set_oauth_app_info(app_id, app_secret, app_uri)
            r.refresh_access_information(APP_REFRESH)
            hello = False
        except:
            print("Retrying")
    print("Log in successful")
    return r

def WPB(FIRSTDAY):
    URL = []
    title = []
    subreddit = []
    for i in xrange(FIRSTDAY,7):
        file = open(str(i))

        t = datetime.datetime.today()
        randMinute = TIMEMINUTE + randint(0,5) + randint(0,5)
        future = datetime.datetime(t.year,t.month,t.day,TIMEHOUR,randMinute)
        if TIMEHOUR <= t.hour and randMinute <= t.minute:
            future += datetime.timedelta(days=1)

        print("wait until " + str(future.month) + " " + str(future.day) + ", " + str(future.year) + " at " + str(TIMEHOUR) + ":" + str(randMinute) + "AM")
        time.sleep((future-t).seconds)

        lineType = 1
        for line in file:
            if lineType == 1:
                URL[:] = []
                URL = line.split("\n")
            elif lineType == 2:
                title[:] = []
                title = line.split("\n")
            elif lineType == 3:
                subreddit[:] = []
                subreddit = line.split()
                postRange = range(0,len(subreddit))
                postRange_iter = iter(postRange)
                for x in postRange_iter:
                    try:
                        post = r.submit(subreddit[x], title[0], url=URL[0])
                        print("posted post " + URL[0] + " (" + title[0] + ") to /r/" + subreddit[x])
                        for NSFWTitles in NSFWPOSTTITLES:  # marks any post as nsfw
                            if title[0] == NSFWTitles:
                                post.mark_as_nsfw()
                                print("marked post " + URL[0] + " (" + title[0] + ") to /r/" + subreddit[x] + " as nsfw")
                        if subreddit[x] == FLAIRSUBS:
                            flair = subreddit[x + 1]
                            r.set_flair(FLAIRSUBS, post, flair_text=flair, flair_css_class=flair)
                            print("flaired post " + URL[0] + " (" + title[0] + ") to /r/" + subreddit[x] + " as " + flair)
                            next(postRange_iter)
                    except:
                        print("Unable to post " + URL[0] + " (" + title[0] + ") to /r/" + subreddit[x])
                time.sleep(2 + randint(0,3))
                lineType = 0       # resets typeOfLine to move on to a new post
            lineType += 1
            time.sleep(POSTDELAY)

def TP(FIRSTDAY):
    URL = []
    title = []
    subreddit = []
    for i in xrange(FIRSTDAY,7):
        file = open(str(i))
        print("Showing day " + str(i) + "'s posts")

        lineType = 1
        for line in file:
            if lineType == 1:
                URL[:] = []
                URL = line.split("\n")
            elif lineType == 2:
                title[:] = []
                title = line.split("\n")
            elif lineType == 3:
                subreddit[:] = []
                subreddit = line.split()
                postRange = range(0,len(subreddit))
                postRange_iter = iter(postRange)
                for x in postRange_iter:
                    try:
                        print("posted post " + URL[0] + " (" + title[0] + ") to /r/" + subreddit[x])
                        for NSFWTitles in NSFWPOSTTITLES:  # marks any post as nsfw
                            if title[0] == NSFWTitles:
                                print("marked post " + URL[0] + " (" + title[0] + ") to /r/" + subreddit[x] + " as nsfw")
                        if subreddit[x] == FLAIRSUBS:
                            flair = subreddit[x + 1]
                            print("flaired post " + URL[0] + " (" + title[0] + ") to /r/" + subreddit[x] + " as " + flair)
                            next(postRange_iter)
                    except:
                        print("Unable to post " + URL[0] + " (" + title[0] + ") to /r/" + subreddit[x])
                lineType = 0       # resets typeOfLine to move on to a new post
            lineType += 1

login()
#TP(0)
#WPB(0)
#TestPosting()