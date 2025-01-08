import praw
import os
from dotenv import load_dotenv
import time
import re
from prawcore.exceptions import PrawcoreException
from requests.exceptions import RequestException

# Load environment variables
load_dotenv()

# Reddit API credentials
try:
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        username=os.getenv('REDDIT_USERNAME'),
        password=os.getenv('REDDIT_PASSWORD'),
        user_agent="ImprovedRedditSearch/1.0"
    )
    print("Successfully connected to Reddit API")
except Exception as e:
    print(f"Error connecting to Reddit API: {str(e)}")
    print("Please check your .env file and ensure all credentials are correct.")
    exit(1)

def search_subreddit(subreddit_name, keywords, limit=100, search_comments=False, timeout=30):
    print(f"Searching r/{subreddit_name} for keywords: {', '.join(keywords)}")
    print(f"Searching in comments: {'Yes' if search_comments else 'No'}")
    
    try:
        subreddit = reddit.subreddit(subreddit_name)
        matching_items = []
        start_time = time.time()

        for post in subreddit.new(limit=limit):
            if time.time() - start_time > timeout:
                print(f"Search timeout reached after {timeout} seconds")
                break

            if matches_keywords(post.title, keywords) or matches_keywords(post.selftext, keywords):
                matching_items.append(format_post(post))
                print(f"Found matching post: {post.title}")

            if search_comments:
                post.comments.replace_more(limit=0)
                for comment in post.comments.list():
                    if matches_keywords(comment.body, keywords):
                        matching_items.append(format_comment(comment, post))
                        print(f"Found matching comment in post: {post.title}")

        print(f"Search completed. Found {len(matching_items)} matching items.")
        return matching_items

    except PrawcoreException as e:
        print(f"Reddit API error: {str(e)}")
    except RequestException as e:
        print(f"Network error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

    return []

def matches_keywords(text, keywords):
    return any(re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE) for keyword in keywords)

def format_post(post):
    return {
        'type': 'post',
        'title': post.title,
        'url': post.url,
        'author': post.author.name if post.author else '[deleted]',
        'score': post.score,
        'created_utc': post.created_utc,
        'body': post.selftext[:500] + '...' if len(post.selftext) > 500 else post.selftext
    }

def format_comment(comment, post):
    return {
        'type': 'comment',
        'post_title': post.title,
        'post_url': post.url,
        'author': comment.author.name if comment.author else '[deleted]',
        'score': comment.score,
        'created_utc': comment.created_utc,
        'body': comment.body[:500] + '...' if len(comment.body) > 500 else comment.body
    }

def monitor_subreddit(subreddit_name, keywords, check_interval=60, search_comments=False):
    print(f"Starting to monitor r/{subreddit_name}")
    print(f"Keywords: {', '.join(keywords)}")
    print(f"Checking every {check_interval} seconds")
    print(f"Searching in comments: {'Yes' if search_comments else 'No'}")
    
    while True:
        try:
            matching_items = search_subreddit(subreddit_name, keywords, search_comments=search_comments)
            
            if matching_items:
                print(f"\nFound {len(matching_items)} matching items in r/{subreddit_name}:")
                for item in matching_items:
                    if item['type'] == 'post':
                        print(f"\nPost: {item['title']}")
                        print(f"URL: {item['url']}")
                        print(f"Author: u/{item['author']}")
                        print(f"Score: {item['score']}")
                        print(f"Created: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['created_utc']))}")
                        print(f"Content: {item['body']}")
                    else:
                        print(f"\nComment on post: {item['post_title']}")
                        print(f"Post URL: {item['post_url']}")
                        print(f"Comment Author: u/{item['author']}")
                        print(f"Comment Score: {item['score']}")
                        print(f"Comment Created: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['created_utc']))}")
                        print(f"Comment Content: {item['body']}")
            else:
                print(f"\nNo matching items found in r/{subreddit_name}")
            
            print(f"\nWaiting for {check_interval} seconds before next check...")
            time.sleep(check_interval)
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user.")
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Waiting for 60 seconds before retrying...")
            time.sleep(60)

if __name__ == "__main__":
    subreddit_name = input("Enter the subreddit name to monitor: ")
    keywords = input("Enter keywords to search for (comma-separated): ").split(',')
    keywords = [keyword.strip() for keyword in keywords]
    search_comments = input("Search in comments as well? (y/n): ").lower() == 'y'
    
    monitor_subreddit(subreddit_name, keywords, search_comments=search_comments)