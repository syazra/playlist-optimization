import csv, random, re
from collections import defaultdict

def contains_non_latin(text):
    pattern = r'[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]'
    return re.search(pattern, text) is not None

def extract_top_songs(input_file, output_file, limit_per_mood=400):
    buckets = defaultdict(list)
    seen_ids = set()
    seen_names = set()

    with open(input_file, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            try:
                bpm = float(row['tempo'])
                duration = round(float(row['duration_ms']) / 60000, 2)
                popularity = int(row['popularity'])
            except ValueError:
                continue

            if not (60 <= bpm <= 140): continue
            if not (1 <= duration <= 10): continue
            if popularity < 1: continue

            track_id = row['track_id']
            track_name = row['track_name'].strip().lower()
            if track_id in seen_ids or track_name in seen_names:
                continue
            artist = row['artists']
            track = row['track_name']
            if contains_non_latin(artist) or contains_non_latin(track):
                continue
            seen_ids.add(track_id)
            seen_names.add(track_name)

            if 60 <= bpm <= 80:
                mood = 'relaksasi'
            elif 80 < bpm <= 120:
                mood = 'fokus'
            else:
                mood = 'energik'

            buckets[mood].append({
                'id':       track_id,
                'artist':   row['artists'],
                'name':     row['track_name'],
                'duration': duration,
                'bpm':      bpm,
                'mood':     mood,
                'score':    popularity
            })

    songs = []
    for mood, bucket in buckets.items():
        bucket.sort(key=lambda x: x['score'], reverse=True)
        top = bucket[:limit_per_mood]
        random.shuffle(top)
        songs.extend(top)
        print(f"{mood}: {len(top)} lagu")

    random.shuffle(songs)

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id','artist','name','duration','bpm','mood','score'])
        writer.writeheader()
        writer.writerows(songs)

    print(f"\nTotal: {len(songs)} lagu → {output_file}")

extract_top_songs('dataset.csv', 'dataset_top300.csv', limit_per_mood=100)