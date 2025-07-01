import os
import requests
import json
from dotenv import load_dotenv
from src.utils import log_event

load_dotenv()

def get_tweets(config):
    headers = {
        "Authorization": f"Bearer {os.getenv('BEARER_TOKEN')}"
    }
    params = {
        "query": config['twitter']['query'],
        "max_results": config['twitter']['max_results'],
        "tweet.fields": config['twitter']['tweet_fields'],
        "expansions": config['twitter']['expansions'],
        "user.fields": config['twitter']['user_fields']
    }

    try:
        response = requests.get("https://api.twitter.com/2/tweets/search/recent", headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        with open(config['output']['raw_path'], "w") as f:
            json.dump(data, f)
        log_event("Tweets successfully extracted.")
        return data
    except Exception as e:
        log_event(f"Error during tweet extraction: {str(e)}", level="ERROR")
        return None
