import os
from dotenv import load_dotenv

load_dotenv()

GROUP_LIST = [g.strip() for g in os.environ["GROUP_LIST"].split(",")]
BASE_URL = os.environ["BASE_URL"]
API_KEY = os.environ["API_KEY"]
MODEL = os.environ["MODEL"]
CHATLOG_EXPORT_ROOT = os.environ["CHATLOG_EXPORT_ROOT"]
OUTPUT_ROOT = os.environ["OUTPUT_ROOT"]
PROMPT_PATH = os.path.join(os.path.dirname(__file__), "聊天记录可视化prompt.md")
