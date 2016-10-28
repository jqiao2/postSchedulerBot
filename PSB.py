import praw
import time
import datetime
import sys

# I don"t have a description for this bot. I"m too lazy :P It is important to
# note that this bot is specialized for me. I may make a generalized version
# if anyone actually sees this and would like one. I just don't need it right
# now.

# post file format:
# post title    [1]
# post URLs     [2]
# subreddit(s)  [3]
# repeat for all posts

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
# List for all the post titles
titles =            []
# Temporary variable for appending titles into array
title =             ""
# List for all the post URLs
URLs =              []
# Temporary variable for appending URLs into array
URL =               ""
# List for all the post subreddits
subreddits =        []
# Temporary variable for appending subreddits into array
subreddit =         []
# Array of posts that have to get tagged NSFW
NSFWPostTitles = 	[]
# Hour time to post (24 hour time)
TIMEHOUR =          4
# Minute time to post minus five
TIMEMINUTE =        15
# Seconds between each post
POSTDELAY =         15

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
        line = line.rstrip("\n")            # removes \n from line
        if typeOfLine == 1:                 # post title
            title = line
            titles.append(title)
        elif typeOfLine == 2:               # URL
            URL = line
            URLs.append(URL)
        elif typeOfLine == 3:               # subreddit
            subreddit = line.split()
            subreddits.append(subreddit[0])
            typeOfLine = 0       # resets typeOfLine to move on to a new post
            # Everything below is for xposting
            numberOfSubreddits = len(subreddit)
            if numberOfSubreddits > 1:
                for x in range(numberOfSubreddits - 1):
                    titles.append(title)
                    URLs.append(URL)
                    subreddits.append(subreddit[x + 1])
        typeOfLine += 1                     # move on to next line type
    # prints for testing
    print(len(titles))
    print(len(URLs))
    print(len(subreddits))

def WPB(FIRSTDAY):
    for i in xrange(FIRSTDAY,7):
        loadPosts(str(i))
        t = datetime.datetime.today()
        randMinute = TIMEMINUTE + randint(0,5) + randint(0,5)
        future = datetime.datetime(t.year,t.month,t.day,TIMEHOUR,randMinute)
        if TIMEHOUR <= t.hour and randMinute <= t.minute:
            future += datetime.timedelta(days=1)
    	
        print(titles[0])
        print("wait until " + str(future.month) + " " + str(future.day) + ", " + str(future.year) + " at " + str(TIMEHOUR) + ":" + str(randMinute) + "AM")
    	time.sleep((future-t).seconds)
    	postRange = range(0,len(titles)) # lets me skip the flair name subreddits 
    	postRange_iter = iter(postRange)
    	for x in postRange_iter:
    		try:
    			post = r.submit(subreddits[x], titles[x], url=URLs[x])
    			print("posted post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x])
    			for NSFWTitles in NSFWPostTitles:  # marks any post as nsfw
    				if titles[x] == NSFWTitles:
    					post.mark_as_nsfw()
    					print("marked post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x] + " as nsfw")
    			if subreddits[x] == "holdthemoan":
    				flair = subreddits[x+1]
    				r.set_flair("holdthemoan", post, flair_text=flair, flair_css_class=flair)
    				print("flaired post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x] + " as " + flair)
    				next(postRange_iter)
    		except:
    			print("Unable to post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x])
    		time.sleep(POSTDELAY)

def TP(FIRSTDAY):
    for i in xrange(FIRSTDAY,7):
        loadPosts(str(i))
        for x in range(0,len(titles)):
            try:
                print("posted post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x])
                if titles[x] == "hi":
                    post.mark_as_nsfw()
                    print("marked post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x] + " as nsfw")
            except:
                print("Unable to post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x])

def TestPosting():
	loadPosts('flairTestFile')
	postRange = range(0,len(titles)) # lets me skip the flair name subreddits 
	postRange_iter = iter(postRange)
	for x in postRange_iter:
		try:
			post = r.submit(subreddits[x], titles[x], url=URLs[x])
			print("posted post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x])
			for NSFWTitles in NSFWPostTitles:  # marks any post as nsfw
				if titles[x] == NSFWTitles:
					post.mark_as_nsfw()
					print("marked post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x] + " as nsfw")
			if subreddits[x] == "holdthemoan":
				flair = subreddits[x+1]
				r.set_flair("holdthemoan", post, flair_text=flair, flair_css_class=flair)
				print("flaired post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x] + " as " + flair)
				next(postRange_iter)
		except:
			print("Unable to post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x])
		time.sleep(POSTDELAY)

login()
#TP(3)
WPB(4)
#TestPosting()