from collections import defaultdict, Counter
import re

#  Common useless words
STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were",
    "in", "on", "at", "to", "for", "of", "and",
    "with", "this", "that", "it", "from", "by",
    "i", "you", "we", "he", "she", "they",
    "my", "your", "his", "her", "their",
    "just", "only", "very", "really"
}


#  Clean text
def clean_text(text):
    return re.sub(r"[^\w\s]", "", text.lower())


#  Extract keywords
def extract_keywords(title):
    words = clean_text(title).split()
    return [w for w in words if w not in STOPWORDS and len(w) > 2]


#  CLUSTER KEY (broad grouping)
def get_cluster_key(title):
    words = extract_keywords(title)

    if not words:
        return "misc"

    #  Only 1–2 words → ensures grouping happens
    return words[0]


#  CLUSTER NAME (human readable)
def extract_phrase(title):
    words = extract_keywords(title)

    if not words:
        return "misc"

    return " ".join(words[:3])


#  Decide best name for cluster
def get_cluster_name(videos):
    phrases = []

    for v in videos:
        phrases.append(extract_phrase(v["title"]))

    return Counter(phrases).most_common(1)[0][0]


#  FINAL CLUSTERING FUNCTION
def cluster_videos(videos):
    clusters = defaultdict(list)

    # STEP 1: group using BROAD key
    for v in videos:
        if not v.get("title"):
            continue

        key = get_cluster_key(v["title"])
        clusters[key].append(v)

    # STEP 2: assign meaningful names
    final_clusters = {}

    for _, vids in clusters.items():
        name = get_cluster_name(vids)
        final_clusters[name] = vids

    return final_clusters