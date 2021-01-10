import logging
import os
from pathlib import Path

# GLOBAL VARIABLES
PROJECT_DIR = Path(__file__).resolve().parents[1]
TEMP_DIR = os.path.join(PROJECT_DIR, 'data', 'temp')
RAW_DIR = os.path.join(PROJECT_DIR, 'data', 'raw')
MODEL_DIR = os.path.join(PROJECT_DIR, 'data', 'model')

# LOGGING CONFIG
class LoggingConfig:
    def __init__(self):
        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt)