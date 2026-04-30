from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["cogni_db"]   

trends_collection = db["trend"]
videos_collection = db["video_db"]
video_trend_map_collection = db["video_trend_map"]