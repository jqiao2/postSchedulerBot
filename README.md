# Post Scheduler Bot

I have no idea how github formatting works, so we'll see how this turns out.

Most of the script's description I put in the header of the script file itself, so if you read this you probably won't have to read that.

This script will post to Reddit everyday by week under some circumstances:

1. If you have enough karma from the subreddit to not get auto-filtered, if you are, your posts won't get posted (the ten minute rule).
2. You put them in right, obviously.

You will need eight other files for this script to work. One is the profile file. This includes all the APP_UA, app_id, etc to associate this script with your Reddit account. The other seven files are the ones that contain your posts for that day (i.e. file 0 contains the posts for day one, file 1 contains the posts for day two, all the way to file 6). There is a specific format these files are to be written in. which is:

1. Post URL
2. Post title
3. Subreddit(s) to post to
4. Continue for all posts

If a subreddit requires you to flair a post, put the flair name after the subreddit name, but also make sure you indicate in the FLAIRSUBS constant, so the script knows to look for a flair after the subreddit name. This only works if you are a mod of that subreddit because that's how I made it...
