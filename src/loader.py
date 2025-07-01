import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from utils import log_event

load_dotenv()

def load_to_postgres(config):
    try:
        df = pd.read_csv(config['output']['processed_path'])

        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )

        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tweets (
                id TEXT PRIMARY KEY,
                clean_text TEXT,
                username TEXT,
                lang TEXT,
                tweet_length INT,
                word_count INT,
                char_count INT,
                followers_count INT,
                following_count INT,
                retweet_count INT,
                like_count INT,
                engagement INT,
                is_high_engagement BOOLEAN,
                text_has_ai BOOLEAN,
                is_verified BOOLEAN,
                day_of_week TEXT,
                hour INT,
                record_loaded_at TIMESTAMP
            );
        """)
        conn.commit()

        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO tweets VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, tuple(row))

        conn.commit()
        cur.close()
        conn.close()
        log_event("Data successfully loaded into PostgreSQL.")
    except Exception as e:
        log_event(f"Error loading to database: {str(e)}", level="ERROR")
