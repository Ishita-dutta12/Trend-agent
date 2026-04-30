import requests
from config import YOUTUBE_API_KEY


def fetch_videos(topic):

    # STEP 1: SEARCH VIDEOS
    search_url = "https://www.googleapis.com/youtube/v3/search"

    search_params = {
        "part": "snippet",
        "q": topic,
        "maxResults": 15,
        "type": "video",
        "key": YOUTUBE_API_KEY
    }

    search_res = requests.get(search_url, params=search_params)
    search_data = search_res.json()

    video_ids = []
    videos_meta = {}

    for item in search_data.get("items", []):
        vid = item["id"]["videoId"]
        video_ids.append(vid)

        videos_meta[vid] = {
            "title": item["snippet"]["title"],
            "platform": "youtube",
            "upload_time": item["snippet"]["publishedAt"]
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
    "url": f"https://www.youtube.com/watch?v={vid}"
})

    return final_videos