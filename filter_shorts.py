import json



with open("data/channel_manifests/code4AI.jsonl", "r", encoding="utf-8") as f:
  for line in f.readlines():
    d = json.loads(line)
    video_id = d["id"]
    duration = d["duration_seconds"]
    print(video_id, duration)
