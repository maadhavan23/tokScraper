import praw
from dotenv import load_dotenv
from pathlib import Path
import re
import os


load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")
print("CLIENT_ID:", os.getenv("REDDIT_CLIENT_ID"))
# Reddit API setup
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def get_top_posts(subreddit_name, keyword, limit=5):
    subreddit = reddit.subreddit(subreddit_name)
    results = []

    for post in subreddit.search(keyword, sort='top', time_filter='week', limit=limit):
        post_data = {
            "title": post.title,
            "url": post.url,
            "description": post.selftext,
            "op_comments": []
        }

        # Fetch OP's comments (author match)
        post.comments.replace_more(limit=0)
        for comment in post.comments:
            if comment.author and comment.author.name == post.author.name:
                post_data["op_comments"].append(comment.body)

        results.append(post_data)

    return results
