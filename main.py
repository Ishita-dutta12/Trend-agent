from fastapi import FastAPI
from ingestion.youtube_ingestion import fetch_videos
from processing.clustering import cluster_videos
from processing.scoring import score_cluster
from processing.ranking import rank_trends
from utils.formatter import build_response
from db.save_data import save_trends
from db.mongo import video_trend_map_collection
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Trend Agent Running"}

from fastapi import Query

@app.get("/trends")
def get_trends(
    topic: str = Query(...),
    creator_url: str = Query(None)
):

    videos = fetch_videos(topic,creator_url)
    print("VIDEOS COUNT:", len(videos))
    clusters = cluster_videos(videos)
    print("CLUSTERS COUNT:", len(clusters))
    trends = []

    for key, vids in clusters.items():
        trends.append({
            "name": key,
            "platform": vids[0]["platform"],
            "viral_score": score_cluster(vids),
            "videos": vids   #  IMPORTANT ADD THIS
        })
    print("TRENDS COUNT:", len(trends))
    ranked = rank_trends(trends)

    #  SAVE TO DB
    cluster_ids = save_trends(ranked[:5], topic)
    print("Mappings count:",
      video_trend_map_collection.count_documents({}))
    return build_response(ranked[:5], topic, cluster_ids)