def rank_trends(trends):
    return sorted(trends, key=lambda x: x["viral_score"], reverse=True)