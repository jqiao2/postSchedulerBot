import praw
import time
import datetime

# This script will post onto Reddit everyday by week if you have enough karma from the subreddit to
# not get auto-blocked. If you are, your posts won't get posted.
# You will need eight separate files for this script to work. One is the profile file. This includes
# all the APP_UA, app_id, etc to associate this script with your Reddit account. The other seven
# files are the ones that contain your posts for that day (i.e. file 0 contains the posts for day
# one, file 1 contains the posts for day two, all the way to file 6). There is a specific format
# these files are to be written in. which is:
# 1. Post URL
# 2. Post title
# 3. Subreddit(s) to post to
# Continue for all posts
# If a subreddit requires you to flair a post, put the flair name after the subreddit name, but
# also make sure you indicate so down below so the script knows to look for a flair after the
# subreddit name. This only works if you are a mod of that subreddit.

# Make your own profile file with all these variables for oauth 2
from PSBProfile import USERAGENT
from PSBProfile import CLIENT_ID
from PSBProfile import PASSWORD
from PSBProfile import CLIENT_SECRET
from PSBProfile import USERNAME
from PSBProfile import FLAIRSUBS

from random import randint

# Reddit instance, logs in for you (I think lol I have no idea)
r = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, password=PASSWORD,
                user_agent=USERAGENT, username=USERNAME)
# List for all the post titles
titles = []
# List for all the post URLs
URLs = []
# List for all the post subreddits
subreddits = []
# Array of posts that have to get tagged NSFW
# I don't need this, but if you do I have no idea if this works
NSFW_POST_TITLES = []
# Name of subreddit(s) that have flairs
# The code only allows you to flair on subreddits with mod permissions
# As you can see, I only need to flair one subreddit, so if you need to flair other subreddits,
# just change it to an array and make the changes to where it is referenced as well
FLAIR_SUBS = FLAIRSUBS
# Hour time to post (24 hour time) 
TIMEHOUR_DEFAULT = 4
TIMEHOUR = TIMEHOUR_DEFAULT
# Minute time to post minus five
TIMEMINUTE_DEFAULT = 15
TIMEMINUTE = TIMEMINUTE_DEFAULT
# Seconds between each post
POSTDELAY_DEFAULT = 15
POSTDELAY = TIMEMINUTE_DEFAULT


def load_posts(day):
    print("Clearing old posts")
    subreddits[:] = []
    titles[:] = []
    URLs[:] = []

    # Temporary variable for appending titles into array
    title = ""
    # Temporary variable for appending URLs into array
    URL = ""
    # Temporary variable for appending subreddits into array
    subreddit = []

    print("Loading posts")
    posts_file = open(day)  # file containing all posts
    type_of_line = 1  # see above; sorts lines
    number_of_posts = 0
    # sorts input into correct array
    for line in posts_file:
        line = line.rstrip("\n")  # removes \n from line
        if type_of_line == 1:  # URL
            URL = line
            URLs.append(URL)
            number_of_posts += 1
        elif type_of_line == 2:  # post title
            title = line
            titles.append(title)
        elif type_of_line == 3:  # subreddit
            subreddit = line.split()
            subreddits.append(subreddit[0])
            type_of_line = 0  # resets type_of_line to move on to a new post
            # Everything below is for crossposting
            number_of_subreddits = len(subreddit)
            if number_of_subreddits > 1:
                for x in range(number_of_subreddits - 1):
                    titles.append(title)
                    URLs.append(URL)
                    subreddits.append(subreddit[x + 1])
        type_of_line += 1  # move on to next line type
    # prints for testing
    print(number_of_posts)
    print(len(titles))


def weekly_post_bot(first_day):
    for i in range(first_day, 7):
        load_posts(str(i))
        t = datetime.datetime.today()
        rand_minute = TIMEMINUTE + randint(0, 5) + randint(0, 5)
        future = datetime.datetime(t.year, t.month, t.day, TIMEHOUR, rand_minute)
        if TIMEHOUR <= t.hour and rand_minute <= t.minute:
            future += datetime.timedelta(days=1)

        print(titles[0])
        print("wait until " + str(future.month) + " " + str(future.day) + ", " + str(
            future.year) + " at " + str(TIMEHOUR) + ":" + str(rand_minute) + "AM")
        time.sleep((future - t).seconds)

        post_range = range(0, len(titles))  # lets me skip the flair name subreddits
        post_range_iter = iter(post_range)
        for x in post_range_iter:
            try:
                post = r.subreddit(subreddits[x]).submit(title=titles[x], url=URLs[x])
                # print("posted post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x])
                print(post)
                for NSFWTitles in NSFW_POST_TITLES:  # marks any post as nsfw
                    if titles[x] == NSFWTitles:
                        post.mark_as_nsfw()
                        print("marked post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[
                            x] + " as nsfw")
                if subreddits[x] == FLAIR_SUBS:
                    flair = subreddits[x + 1]
                    post.mod.flair(text=flair, css_class=flair)
                    print("flaired post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[
                        x] + " as " + flair)
                    next(post_range_iter)
            except:
                print("Unable to post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x])
            time.sleep(POSTDELAY)


def test_post(first_day):
    for i in range(first_day, 7):
        load_posts(str(i))
        post_range = range(0, len(titles))  # lets me skip the flair name subreddits
        post_range_iter = iter(post_range)
        for x in post_range_iter:
            try:
                print("posted post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x])
                if subreddits[x] == FLAIR_SUBS:
                    flair = subreddits[x + 1]
                    print("flaired post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[
                        x] + " as " + flair)
                    next(post_range_iter)
            except:
                print("Unable to post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x])


# I have no idea if this function still works i.e. test it
def post_single_day(day):
    load_posts(day)

    t = datetime.datetime.today()
    rand_minute = TIMEMINUTE + randint(0, 5) + randint(0, 5)
    future = datetime.datetime(t.year, t.month, t.day, TIMEHOUR, rand_minute)
    if TIMEHOUR <= t.hour and rand_minute <= t.minute:
        future += datetime.timedelta(days=1)

    print(titles[0])
    print("wait until " + str(future.month) + " " + str(future.day) + ", " + str(
        future.year) + " at " + str(TIMEHOUR) + ":" + str(rand_minute) + "AM")
    time.sleep((future - t).seconds)

    post_range = range(0, len(titles))  # lets me skip the flair name subreddits
    post_range_iter = iter(post_range)
    for x in post_range_iter:
        try:
            post = r.subreddit(subreddits[x]).submit(title=titles[x], url=URLs[x])
            print("posted post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x])
            for NSFWTitles in NSFW_POST_TITLES:  # marks any post as nsfw
                if titles[x] == NSFWTitles:
                    post.mark_as_nsfw()
                    print("marked post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[
                        x] + " as nsfw")
            if subreddits[x] == FLAIR_SUBS:
                flair = subreddits[x + 1]
                post.mod.flair(text=flair, css_class=flair)
                print("flaired post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[
                    x] + " as " + flair)
                next(post_range_iter)
        except:
            print("Unable to post " + URLs[x] + " (" + titles[x] + ") to /r/" + subreddits[x])
        time.sleep(POSTDELAY)


def post():
    post = r.subreddit("exoticmind").submit(title="test", selftext="hello")
    print(post)


# All input is the day to start on (0 = Monday, etc etc)
# actual posting function, constructor corresponds to the day you're on
# weekly_post_bot(0)
# used to make sure the files are named properly
test_post(0)
# posts a single day
# test_posting(0)
# post()
