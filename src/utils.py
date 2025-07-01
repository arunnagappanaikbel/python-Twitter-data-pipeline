import logging
import os

def log_event(message, level="INFO"):
    logging.basicConfig(filename='data/logs/etl.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)
    getattr(logging, level.lower())(message)
    