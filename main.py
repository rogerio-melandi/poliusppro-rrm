from dotenv import load_dotenv
from client_reddit import ClientReddit
import os
import boto3

load_dotenv()

reddit = ClientReddit(
    client_id=os.environ.get("REDDIT_CLIENT_KEY"),
    client_secret=os.environ.get("REDDIT_SECRET_KEY"),
    username=os.environ.get("REDDIT_USERNAME"),
    password=os.environ.get("REDDIT_PASSWORD"),
    user_agent=os.environ.get("REDDIT_USER_AGENT"),
)

posts = reddit.get_hot_posts(os.environ.get("REDDIT_SUBREDDIT"), limit=5)

subs = os.environ.get("REDDIT_SUBREDDIT")

CSV_PATH = f"{subs}.csv"

posts.to_csv(CSV_PATH, sep="|", index=False)

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)

s3.upload_file(
    CSV_PATH, os.environ.get("AWS_S3_BUCKET_NAME"), f"subreddits_raw/{CSV_PATH}"
)
