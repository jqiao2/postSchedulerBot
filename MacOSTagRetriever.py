from xattr import xattr
from pathlib import Path
from biplist import readPlistFromString
import re

pathlist = Path(
    '/Users/JasonQiao/Documents/Reddit/RedditBots/testingFile/New Folder With Items 2').glob(
    '*.jpg')

for path in pathlist:
    str_path = str(path)

    file_name = str_path[81:]
    print(file_name)

    subreddits = readPlistFromString(xattr(str_path).get('com.apple.metadata:_kMDItemUserTags'))
    for subreddit in subreddits:
        print(re.compile('[^a-zA-Z_]+').sub('', subreddit))
    print()
