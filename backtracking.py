from load_data import load_songs_from_csv
import time

def backtrack_recursive(idx, current, cur_dur, cur_score, songs, max_duration, best):
    best['nodes'] += 1
    if cur_score > best['score']:
        best['score'] = cur_score
        best['playlist'] = current[:]

    for i in range(idx, len(songs)):
        song = songs[i]
        if cur_dur + song['duration'] > max_duration:
            best['pruned'] += 1
            continue
        current.append(song)
        backtrack_recursive(i + 1, current, cur_dur + song['duration'], cur_score + song['score'], songs, max_duration, best)
        current.pop()

def backtracking_playlist(songs, max_duration, target_mood):
    songs = [s for s in songs if s['mood'] == target_mood]
    best = {'score': 0, 'playlist': [], 'nodes': 0, 'pruned': 0}
    backtrack_recursive(0, [], 0, 0, songs, max_duration, best)
    return best['playlist'], best['score'], best['nodes'], best['pruned']

# ===== MAIN =====
target_mood = 'relaksasi'
max_duration = 60
n = 50
songs = load_songs_from_csv('dataset_top300.csv', n)

start = time.perf_counter()
bt_playlist, bt_score, bt_nodes, bt_pruned = backtracking_playlist(songs, max_duration, target_mood)
end = time.perf_counter()

print("=================================== BACKTRACKING RESULT ===================================")
print(f"Jumlah Dataset   : {n}")
print(f"Target Mood      : {target_mood}")
print(f"Batas Durasi     : {max_duration} menit")
print("===========================================================================================")
print(f"Skor Popularity  : {bt_score}")
print(f"Jumlah Node      : {bt_nodes}")
print(f"Node Dipangkas   : {bt_pruned}")
print(f"Time Execution   : {end - start}")
print("===========================================================================================")
print("Playlist Terbaik :")
print("===========================================================================================")

total_duration = 0
for i, s in enumerate(bt_playlist, start=1):
    total_duration += s['duration']
    artist = s['artist'][:20] + '..' if len(s['artist']) > 20 else s['artist']
    name   = s['name'][:30]   + '..' if len(s['name'])   > 30 else s['name']
    print(f"{i:>2}. {artist:<22} | {name:<32} | {s['duration']:>4} mnt | {s['bpm']:>6.1f} BPM | {s['score']:>3}")

print("===========================================================================================")
print(f"Total Lagu       : {len(bt_playlist)}")
print(f"Total Durasi     : {round(total_duration, 2)} menit")
print("===========================================================================================")