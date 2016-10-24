import praw
import time
import datetime
import sys

# I don't have a description for this bot. I'm too lazy :P

# post file format:
# post title    [1]
# post URLs     [2]
# subreddit(s)  [3]
# repeat for all posts

# Make your own profile file with all these variables for oauth 2
from profile import APP_UA
from profile import app_id
from profile import app_secret
from profile import app_uri
from profile import app_scopes
from profile import app_account_code
from profile import APP_REFRESH

r =                 praw.Reddit(APP_UA)
titles =            []      # list for all the post titles
title =             ''      # temporary variable for appending titles into array
URLs =              []      # list for all the post URLs
URL =               ''      # temporary variable for appending URLs into array
subreddits =        []      # list for all the post subreddits
subreddit =         []      # temporary variable for appending subreddits into array
TIMEHOUR =          4       # hour time to post (24 hour time)
TIMEMINUTE =        20      # minute time to post
POSTDELAY =         15      # seconds between each post

def login():
    print("Logging into reddit")
    r.set_oauth_app_info(app_id, app_secret, app_uri)
    r.refresh_access_information(APP_REFRESH)
    print("Log in successful")
    return r

def loadPosts(day):
    print("Clearing old posts")
    subreddits[:] = []
    titles[:] = []
    URLs[:] = []

    print("Loading posts")
    postsfile =     open(day)               # file containing all posts
    typeOfLine =    1;                      # see above; sorts lines
    # sorts input into correct array
    for line in postsfile:
        line = line.rstrip('\n')            # removes \n from line
        if typeOfLine == 1:                 # post title
            title = line
            titles.append(title)
        elif typeOfLine == 2:               # URL
            URL = line
            URLs.append(URL)
        elif typeOfLine == 3:               # subreddit; loads in multiple subreddits with titles/URLs if necessary
            subreddit = line.split()
            isholdthemoan(subreddit)
            subreddits.append(subreddit[0])
            typeOfLine = 0                  # resets typeOfLine because we move on to a new post
            # Everything below is only for xposting
            numberOfSubreddits = len(subreddit)
            if numberOfSubreddits > 1:
                for x in range(numberOfSubreddits - 1):
                    titles.append(title)
                    URLs.append(URL)
                    isholdthemoan(subreddit[x+1])
                    subreddits.append(subreddit[x + 1])
        typeOfLine += 1                     # move on to next line type
    # prints for testing
    print(len(titles))
    print(len(URLs))
    print(len(subreddits))

def isholdthemoan(sc):
    if sc == 'holdthemoan':
        print("make sure the post title contains [GIF] or [IMG]")

def postbot():
    # This function is somewhat defunct

    # if for some reason this script is still running
    # after a year, we'll stop after 365 days
    loadPosts(str(0))
    for i in xrange(0,365):
        # sleep until specified time
        t = datetime.datetime.today()
        future = datetime.datetime(t.year,t.month,t.day,TIMEHOUR,TIMEMINUTE)
        if t.hour >= TIMEHOUR:
            future += datetime.timedelta(days=1)
        print("wait until " + str(TIMEHOUR) + ":" + str(TIMEMINUTE) + "AM")
        time.sleep((future-t).seconds)
        # do stuff at specified time
        user = r.get_redditor('exoticmind_2')   # Retrieve post and comment karma
        print(user.link_karma)
        print(user.comment_karma)
        for x in range(0,len(titles)):
            try:
                r.submit(subreddits[x], titles[x], url=URLs[x])
                print("posted post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x])
            except:
                print('Unable to post ' + URLs[x] + ' (' + titles[x] + ') to /r/' + subreddits[x])
            time.sleep(POSTDELAY)

def WPB(FIRSTDAY):
    for i in xrange(FIRSTDAY,7):
        loadPosts(str(i))

        t = datetime.datetime.today()
        future = datetime.datetime(t.year,t.month,t.day + 1,TIMEHOUR,TIMEMINUTE)
        #future += datetime.timedelta(days=1)
        print("wait until " + str(future.month) + " " + str(future.day) + ", " + str(future.year) + " at " + str(TIMEHOUR) + ":" + str(TIMEMINUTE) + "AM")
        time.sleep((future-t).seconds)
        for x in range(0,len(titles)):
            try:
                post = r.submit(subreddits[x], titles[x], url=URLs[x])
                print("posted post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x])
                if titles[x] == 'hi':
                    post.mark_as_nsfw()
                    print("marked post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x] + " as nsfw")
            except:
                print('Unable to post ' + URLs[x] + ' (' + titles[x] + ') to /r/' + subreddits[x])
            time.sleep(POSTDELAY)

def TP(FIRSTDAY):
    for i in xrange(FIRSTDAY,7):
        loadPosts(str(i))
        for x in range(0,len(titles)):
            try:
                print("posted post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x])
                if titles[x] == 'hi':
                    post.mark_as_nsfw()
                    print("marked post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x] + " as nsfw")
            except:
                print('Unable to post ' + URLs[x] + ' (' + titles[x] + ') to /r/' + subreddits[x])
            
login()
#TP(0)
#WPB(0)