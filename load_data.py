import csv

def load_songs_from_csv(filepath, limit=None):
    songs = []
    with open(filepath, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            
            songs.append({
                'id':       row['id'],
                'artist':   row['artist'],
                'name':     row['name'],
                'duration': float(row['duration']),
                'bpm':      float(row['bpm']),
                'mood':     row['mood'],
                'score':    int(row['score'])
            })

            if limit and len(songs) >= limit:
                break

    return songs