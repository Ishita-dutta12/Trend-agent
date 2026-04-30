from datetime import datetime

def calculate_freshness(upload_time):
    now = datetime.utcnow()
    upload = datetime.fromisoformat(upload_time.replace("Z", ""))

    hours = (now - upload).total_seconds() / 3600

    # Freshness score (recent = higher)
    if hours < 24:
        return 30
    elif hours < 72:
        return 20
    elif hours < 168:  # 7 days
        return 10
    else:
        return 5


def score_cluster(videos):

    total_views = sum(v["views"] for v in videos)
    total_likes = sum(v["likes"] for v in videos)
    total_comments = sum(v["comments"] for v in videos)

    avg_views = total_views / len(videos)

    # Engagement ratio
    engagement_rate = (total_likes + total_comments) / max(total_views, 1)

    # Freshness (average of cluster)
    freshness_scores = [
        calculate_freshness(v["upload_time"]) for v in videos
    ]
    avg_freshness = sum(freshness_scores) / len(freshness_scores)

    score = (
        min(avg_views / 1e6, 40) +          # views
        min(engagement_rate * 100, 30) +    # engagement
        avg_freshness                      # freshness
    )

    return round(min(score, 100), 1)