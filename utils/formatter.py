from datetime import datetime
import uuid

def build_response(trends, niche, cluster_ids=None):

    output = []

    for i, t in enumerate(trends):
        cluster_id = cluster_ids[i] if cluster_ids else None
        output.append({
            "trend_id": str(uuid.uuid4()),
            "cluster_id": cluster_id,
            "rank": i + 1,
            "platform": t["platform"],
            "name": t["name"],
            "category": niche,
            "type": "video_topic",
            "keywords": [t["name"]],
            "viral_score": t["viral_score"],
            "lifecycle_stage": "hot" if t["viral_score"] > 80 else "growing",
            "hook_suggestion": f"Start your video with: {t['name']}",
            "audio_id": None,
            "platform_formats": ["short_video", "reel"],
            "detected_at": datetime.utcnow().isoformat()
        })

    return {
        "creator_niche": niche,
        "top_trends": output,
        "virality_confidence": round(
            sum(t["viral_score"] for t in trends) / len(trends), 1
        ) if trends else 0
    }