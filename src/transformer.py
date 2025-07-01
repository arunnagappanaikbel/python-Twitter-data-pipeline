import pandas as pd
import re
import json
from utils import log_event
from datetime import datetime

def clean_text(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text.strip().lower()

def extract_transform(config):
    try:
        with open(config['output']['raw_path'], "r") as f:
            data = json.load(f)

        tweets = pd.json_normalize(data, record_path=['data'])
        users = pd.json_normalize(data, record_path=['includes', 'users'])

        # Merge users
        df = tweets.merge(users, left_on="author_id", right_on="id", suffixes=("", "_user"))

        # Complex transformations
        df['clean_text'] = df['text'].apply(clean_text)
        df['tweet_length'] = df['clean_text'].apply(len)
        df['word_count'] = df['clean_text'].apply(lambda x: len(x.split()))
        df['char_count'] = df['clean_text'].apply(len)
        df['created_at'] = pd.to_datetime(df['created_at'])
        df['hour'] = df['created_at'].dt.hour
        df['day_of_week'] = df['created_at'].dt.day_name()
        df['is_verified'] = df['verified']
        df['followers_count'] = df['public_metrics_user'].apply(lambda x: x.get("followers_count", 0))
        df['following_count'] = df['public_metrics_user'].apply(lambda x: x.get("following_count", 0))
        df['retweet_count'] = df['public_metrics'].apply(lambda x: x.get("retweet_count", 0))
        df['like_count'] = df['public_metrics'].apply(lambda x: x.get("like_count", 0))
        df['engagement'] = df['retweet_count'] + df['like_count']
        df['is_high_engagement'] = df['engagement'] > df['engagement'].quantile(0.75)
        df['text_has_ai'] = df['clean_text'].apply(lambda x: "ai" in x)
        df['username'] = df['username']
        df['lang'] = df['lang']
        df['date'] = df['created_at'].dt.date
        df['time'] = df['created_at'].dt.time
        df['record_loaded_at'] = datetime.now()

        selected_cols = ['id', 'clean_text', 'username', 'lang', 'tweet_length', 'word_count', 'char_count',
                         'followers_count', 'following_count', 'retweet_count', 'like_count', 'engagement',
                         'is_high_engagement', 'text_has_ai', 'is_verified', 'day_of_week', 'hour',
                         'record_loaded_at']

        df[selected_cols].to_csv(config['output']['processed_path'], index=False)
        log_event("Tweets transformed and saved.")
        return df[selected_cols]

    except Exception as e:
        log_event(f"Error during transformation: {str(e)}", level="ERROR")
        return None
