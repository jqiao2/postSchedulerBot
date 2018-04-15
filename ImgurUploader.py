IMGUR_CLIENT_ID = "740158d2090defc"
IMGUR_CLIENT_SECRET = "34ebe78d8496546830bc4c9736d03ced0d7a495f"
IMGUR_ACCESS_TOKEN = "36a4610518ef9e04ccd7bbae864cf6e5d7361cf4"
IMGUR_REFRESH_TOKEN = "92974b6090704273a6c3206302d949e758fb2baa"

from imgurpython import ImgurClient
from pathlib import Path

client = ImgurClient(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET, IMGUR_ACCESS_TOKEN, IMGUR_REFRESH_TOKEN)
pathlist = Path('/Users/JasonQiao/Documents/Reddit/RedditBots/testingFile/Food').glob('Pizzadilla.png')

def upload_file(file_path):
	config = {'name': file_path[62:-4]}
	return client.upload_from_path(file_path, config = config, anon = False)

for path in pathlist:
	str_path = str(path)
	image = upload_file(str_path)
	print("uploaded", str_path[62:-4])
	# image_link = image['link']
	print(image)