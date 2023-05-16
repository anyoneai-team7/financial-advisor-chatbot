from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv


DATASET_ROOT_PATH = str(Path(__file__).parent.parent.parent / "data")
DATA_RAW_PATH = str(Path(DATASET_ROOT_PATH) / "raw")
DATA_PROCESSED_PATH = str(Path(DATASET_ROOT_PATH) / "processed")
BUCKET_NAME = "anyoneai-datasets"
S3_FOLDER_URL = "nasdaq_annual_reports/"

# load ChatGPT_Key from .env
load_dotenv()
_ = load_dotenv(find_dotenv())

API_KEY = os.getenv("GPT_KEY")
