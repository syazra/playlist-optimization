from load_data import load_songs_from_csv
import time

def brute_force_recursive(idx, cur_dur, cur_score, songs, max_duration, best):
    best['nodes'] += 1

    if idx == len(songs):
        if cur_dur <= max_duration and cur_score > best['score']:
            best['score'] = cur_score
            best['playlist'] = best['current'][:]
        return

    song = songs[idx]
    
    best['current'].append(song)
    brute_force_recursive(idx + 1, cur_dur + song['duration'], cur_score + song['score'], songs, max_duration, best)
    best['current'].pop()
    
    brute_force_recursive(idx + 1, cur_dur, cur_score, songs, max_duration, best)
    
def brute_force_playlist(songs, max_duration, target_mood):
    songs = [s for s in songs if s['mood'] == target_mood]
    best = {'score': 0, 'playlist': [], 'current': [], 'nodes': 0}
    brute_force_recursive(0, 0, 0, songs, max_duration, best)
    return best['playlist'], best['score'], best['nodes']

# ===== MAIN =====
target_mood = 'relaksasi'
max_duration = 60
n = 50
songs = load_songs_from_csv('dataset_top300.csv', n)

start = time.perf_counter()
bf_playlist, bf_score, bf_nodes = brute_force_playlist(songs, max_duration, target_mood)
end = time.perf_counter()

print("=================================== BRUTE FORCE RESULT ===================================")
print(f"Jumlah Dataset   : {n}")
print(f"Target Mood      : {target_mood}")
print(f"Batas Durasi     : {max_duration} menit")
print("===========================================================================================")
print(f"Skor Popularity  : {bf_score}")
print(f"Node Dikunjungi  : {bf_nodes}")
print(f"Time Execution   : {end - start}")
print("===========================================================================================")
print("Playlist Terbaik :")
print("===========================================================================================")

total_duration = 0
for i, s in enumerate(bf_playlist, start=1):
    total_duration += s['duration']
    artist = s['artist'][:20] + '..' if len(s['artist']) > 20 else s['artist']
    name   = s['name'][:30]   + '..' if len(s['name'])   > 30 else s['name']
    print(f"{i:>2}. {artist:<22} | {name:<32} | {s['duration']:>4} mnt | {s['bpm']:>6.1f} BPM | {s['score']:>3}")

print("===========================================================================================")
print(f"Total Lagu       : {len(bf_playlist)}")
print(f"Total Durasi     : {round(total_duration, 2)} menit")
print("===========================================================================================")