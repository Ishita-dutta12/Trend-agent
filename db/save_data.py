import uuid
from datetime import datetime
from db.mongo import trends_collection, videos_collection, video_trend_map_collection

print("save_trends CALLED")
def save_trends(trends, niche):

    cluster_ids = []

    for t in trends:

        cluster_id = str(uuid.uuid4())
        print("Saving cluster:", cluster_id)
        #  1. SAVE TREND
        trends_collection.insert_one({
            "_id": cluster_id,
            "trend_id": cluster_id,
            "name": t["name"],
            "category": niche,
            "platform": t["platform"],
            "viral_score": t["viral_score"],
            "created_at": datetime.utcnow()
        })

        #  2. SAVE VIDEOS + MAP
        for v in t["videos"]:

            video_id = v["video_id"]
            print("Videos in cluster:", len(t["videos"]))
            print("Mapping:", cluster_id, "->", video_id)
            # Save video (no cluster_id here now)
            videos_collection.update_one(
                {"_id": video_id},
                {
                    "$set": {
                        "video_id": v["video_id"],          
                        "creator_id": v.get("creator_id", "unknown"),  
                        "title": v["title"],
                        "url": v["url"],
                        "views": v["views"],
                        "likes": v["likes"],
                        "comments": v["comments"],
                        "upload_time": v["upload_time"]
                    }
                },
                upsert=True
            )

            #  3. SAVE MAPPING
            video_trend_map_collection.insert_one({
                "id": str(uuid.uuid4()),        
                "trend_id": cluster_id,         
                "video_id": video_id 
            })

        cluster_ids.append(cluster_id)

    return cluster_ids