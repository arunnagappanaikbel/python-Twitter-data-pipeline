import yaml
from src.extractor import get_tweets
from src.transformer import extract_transform
from src.loader import load_to_postgres

if __name__ == "__main__":
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    data = get_tweets(config)
    if data:
        df = extract_transform(config)
        if df is not None:
            load_to_postgres(config)
