import requests
from config import YOUTUBE_API_KEY


#  MAIN FUNCTION
def fetch_videos(topic, creator_url=None):

    #  If creator is given → extract channel_id
    channel_id = None
    if creator_url:
        channel_id = extract_channel_id(creator_url)

    # STEP 1: SEARCH VIDEOS
    search_url = "https://www.googleapis.com/youtube/v3/search"

    search_params = {
        "part": "snippet",
        "q": topic,
        "maxResults": 15,
        "type": "video",
        "key": YOUTUBE_API_KEY
    }

    # 
    if channel_id:
        search_params["channelId"] = channel_id

    search_res = requests.get(search_url, params=search_params)
    search_data = search_res.json()

    video_ids = []
    videos_meta = {}

    for item in search_data.get("items", []):
        vid = item["id"]["videoId"]
        snippet = item["snippet"]

        video_ids.append(vid)

        videos_meta[vid] = {
            "title": snippet["title"],
            "platform": "youtube",
            "upload_time": snippet["publishedAt"],
            "creator_id": snippet["channelId"]   # 🔥 IMPORTANT
        }

    if not video_ids:
        return []

    # STEP 2: GET STATISTICS
    stats_url = "https://www.googleapis.com/youtube/v3/videos"

    stats_params = {
        "part": "statistics",
        "id": ",".join(video_ids),
        "key": YOUTUBE_API_KEY
    }

    stats_res = requests.get(stats_url, params=stats_params)
    stats_data = stats_res.json()

    final_videos = []

    for item in stats_data.get("items", []):
        vid = item["id"]
        stats = item.get("statistics", {})

        final_videos.append({
            "video_id": vid,
            "title": videos_meta[vid]["title"],
            "platform": "youtube",
            "views": int(stats.get("viewCount", 0)),
            "likes": int(stats.get("likeCount", 0)),
            "comments": int(stats.get("commentCount", 0)),
            "upload_time": videos_meta[vid]["upload_time"],
            "url": f"https://www.youtube.com/watch?v={vid}",
            "creator_id": videos_meta[vid]["creator_id"]   # 🔥 REQUIRED for DB
        })

    return final_videos


#  EXTRACT CHANNEL ID FROM CREATOR URL
def extract_channel_id(url):

    # Case 1: @username format
    if "@" in url:
        username = url.split("@")[-1]

        search_url = "https://www.googleapis.com/youtube/v3/search"

        params = {
            "part": "snippet",
            "q": username,
            "type": "channel",
            "maxResults": 1,
            "key": YOUTUBE_API_KEY
        }

        res = requests.get(search_url, params=params)
        data = res.json()

        if data.get("items"):
            return data["items"][0]["snippet"]["channelId"]

    # Case 2: channelId already in URL
    if "channel/" in url:
        return url.split("channel/")[-1]

    return None