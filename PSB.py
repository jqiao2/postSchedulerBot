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
from PSBProfile import USERAGENT
from PSBProfile import CLIENT_ID
from PSBProfile import PASSWORD
from PSBProfile import CLIENT_SECRET
from PSBProfile import USERNAME

from random import randint

# Reddit instance, logs in for you (I think lol I have no idea)
r =                     praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, password=PASSWORD, user_agent=USERAGENT, username=USERNAME)
# List for all the post titles
titles =                []
# List for all the post URLs
URLs =                  []
# List for all the post subreddits
subreddits =            []
# Array of posts that have to get tagged NSFW
# I don't need this, but if you do I have no idea if this works
NSFWPOSTTITLES =        []
# Name of subreddit(s) that have flairs
# The code only allows you to flair on subreddits with mod permissions
# As you can see, I only need to flair holdthemoan posts, so if you need to flair
# other subreddits, just change it to an array and make the changes to where
# it is referenced as well
FLAIRSUBS =             "holdthemoan"
# Hour time to post (24 hour time) 
TIMEHOUR_DEFAULT =      4
TIMEHOUR =              TIMEHOUR_DEFAULT
# Minute time to post minus five
TIMEMINUTE_DEFAULT =    15
TIMEMINUTE =            TIMEMINUTE_DEFAULT
# Seconds between each post
POSTDELAY_DEFAULT =     15
POSTDELAY =             TIMEMINUTE_DEFAULT

def loadPosts(day):
    print("Clearing old posts")
    subreddits[:] = []
    titles[:] = []
    URLs[:] = []

    # Temporary variable for appending titles into array
    title =         ""
    # Temporary variable for appending URLs into array
    URL =           ""
    # Temporary variable for appending subreddits into array
    subreddit =     []

    print("Loading posts")
    postsfile =     open(day)               # file containing all posts
    typeOfLine =    1;                      # see above; sorts lines
    numberOfPosts = 0;
    # sorts input into correct array
    for line in postsfile:
        line = line.rstrip("\n")            # removes \n from line
        if typeOfLine == 1:                 # URL
            URL = line
            URLs.append(URL)

            numberOfPosts += 1;
        elif typeOfLine == 2:               # post title
            title = line
            titles.append(title)
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
    print(numberOfPosts)
    print(len(titles))

def WPB(FIRSTDAY):
    for i in range(FIRSTDAY,7):
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
                post = r.subreddit(subreddits[x]).submit(title = titles[x], url = URLs[x])
                print("posted post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x])
                for NSFWTitles in NSFWPOSTTITLES:  # marks any post as nsfw
                    if titles[x] == NSFWTitles:
                        post.mark_as_nsfw()
                        print("marked post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x] + " as nsfw")
                if subreddits[x] == FLAIRSUBS:
                    flair = subreddits[x+1]
                    post.mod.flair(text=flair, css_class=flair)
                    print("flaired post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x] + " as " + flair)
                    next(postRange_iter)
            except:
                print("Unable to post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x])
            time.sleep(POSTDELAY)

def TP(FIRSTDAY):
    for i in range(FIRSTDAY,7):
        loadPosts(str(i))
        postRange = range(0,len(titles)) # lets me skip the flair name subreddits 
        postRange_iter = iter(postRange)
        for x in postRange_iter:
            try:
                print("posted post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x])
                if subreddits[x] == FLAIRSUBS:
                    flair = subreddits[x+1]
                    print("flaired post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x] + " as " + flair)
                    next(postRange_iter)
            except:
                print("Unable to post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x])

# I have no idea if this function still works i.e. test it
def PostSingleDay(DAY):
    loadPosts(DAY)
    
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
            post = r.subreddit(subreddits[x]).submit(title = titles[x], url = URLs[x])
            print("posted post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x])
            for NSFWTitles in NSFWPOSTTITLES:  # marks any post as nsfw
                if titles[x] == NSFWTitles:
                    post.mark_as_nsfw()
                    print("marked post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x] + " as nsfw")
            if subreddits[x] == FLAIRSUBS:
                flair = subreddits[x+1]
                post.mod.flair(text=flair, css_class=flair)
                print("flaired post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x] + " as " + flair)
                next(postRange_iter)
        except:
            print("Unable to post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x])
        time.sleep(POSTDELAY)

# All input is the day to start on (0 = Monday, etc etc)
# actual posting function, constructor corresponds to the day you're on
# WPB(0)
# used to make sure the files are named properly
TP(0)
# posts a single day
# TestPosting(0)