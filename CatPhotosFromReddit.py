import praw
import requests
import os
import hashlib
from fake_useragent import UserAgent

ua = UserAgent()
fake_user_agent = ua.random  # Generate a random user agent

# Reddit API credentials
CLIENT_ID = 'CLIENT_ID'
CLIENT_SECRET = 'CLIENT_SECRET'

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=fake_user_agent)

# List of subreddits from where the photos will be downloaded
subreddits = ['cat', 'cats']

photos_dir = "photos"
if not os.path.exists(photos_dir):
    os.makedirs(photos_dir)

downloaded_images = set()

def get_image_hash(image_content):
    return hashlib.md5(image_content).hexdigest()

def load_existing_hashes():
    for filename in os.listdir(photos_dir):
        filepath = os.path.join(photos_dir, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'rb') as img_file:
                content = img_file.read()
                image_hash = get_image_hash(content)
                downloaded_images.add(image_hash)

def download_image(url, filepath):
    headers = {'User-Agent': fake_user_agent}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        image_hash = get_image_hash(response.content)

        if image_hash in downloaded_images:
            print(f"Image already downloaded, skipping: {url}")
        else:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            downloaded_images.add(image_hash)
            print(f"Downloaded {filepath}")
    else:
        print(f"Failed to download {url}")


load_existing_hashes()


for subreddit in subreddits:
    print(f"Fetching latest posts from {subreddit}")
    for submission in reddit.subreddit(subreddit).new(limit=10):  # Change the limit to get the desired ammount of photos
        if submission.url.endswith(('jpg', 'jpeg', 'png')):
            image_name = submission.url.split('/')[-1]
            file_path = os.path.join(photos_dir, image_name)
            if not os.path.exists(file_path):
                download_image(submission.url, file_path)

print("Download complete.")