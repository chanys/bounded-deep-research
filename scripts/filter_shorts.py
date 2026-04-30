import json
import glob
import os.path

shorts_ids = set()
video_ids = set()
with open("data/channel_manifests/code4AI.jsonl", "r", encoding="utf-8") as f:
    for line in f.readlines():
        d = json.loads(line)
        video_id = d["id"]
        duration = d["duration_seconds"]
        if duration <= 180:
            shorts_ids.add(video_id)
        video_ids.add(video_id)

# check whether there are any shorts in data/chunks
# for filepath in glob.glob("data/chunks/*"):
#     filename = os.path.basename(filepath)
#     filename_base = filename.split(".")[0]
#     if filename_base in shorts_ids:
#         print(filepath)
#
#
# # check whether there are any shorts in data/transcripts
# for filepath in glob.glob("data/transcripts/*"):
#     filename = os.path.basename(filepath)
#     filename_base = filename.split(".")[0]
#     if filename_base in shorts_ids:
#         print(filepath)


import shutil

dest_dir = "data/transcripts/code4AI"
os.makedirs(dest_dir, exist_ok=True)

moved = 0
for filepath in glob.glob("data/transcripts/*"):
    # Skip directories — don't try to move data/transcripts/code4AI into itself.
    if os.path.isdir(filepath):
        continue

    filename = os.path.basename(filepath)
    filename_base = filename.split(".")[0]
    if filename_base in video_ids:
        dest = os.path.join(dest_dir, filename)
        shutil.move(filepath, dest)
        print(f"{filename} -> {dest}")
        moved += 1

print(f"Moved {moved} files to {dest_dir}")