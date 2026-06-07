import math
import random
import time
from load_data import load_songs_from_csv

def objective_function(playlist, max_duration, target_mood):
    dur = sum(s['duration'] for s in playlist)
    if dur > max_duration:
        return -9999
    return sum(s['score'] for s in playlist if s['mood'] == target_mood)

def get_neighbor(current, filtered):
    neighbor = current[:]
    neighbor_ids = {s['id'] for s in neighbor}
    candidates = [s for s in filtered if s['id'] not in neighbor_ids]

    op = random.choice(['add', 'remove', 'swap'])
    if op == 'add' and candidates:
        neighbor.append(random.choice(candidates))
    elif op == 'remove' and len(neighbor) > 1:
        neighbor.pop(random.randint(0, len(neighbor) - 1))
    elif op == 'swap' and neighbor and candidates:
        neighbor[random.randint(0, len(neighbor) - 1)] = random.choice(candidates)

    return neighbor

def simulated_annealing(songs, max_duration, target_mood, T, alpha, T_min):
    filtered = [s for s in songs if s['mood'] == target_mood]
    if not filtered:
        return [], 0, 0

    best = filtered[:max(1, len(filtered) // 3)]
    best_eval = objective_function(best, max_duration, target_mood)
    current, current_eval = best[:], best_eval

    while T > T_min:
        candidate = get_neighbor(current, filtered)
        candidate_eval = objective_function(candidate, max_duration, target_mood)

        if candidate_eval > current_eval or random.random() < math.exp((candidate_eval - current_eval) / T):
            current, current_eval = candidate, candidate_eval
            
            if current_eval > best_eval:
                best, best_eval = current[:], current_eval

        T *= alpha

    return best, best_eval
   
# ===== MAIN =====
target_mood = 'fokus'
max_duration = 30
n = 80
songs = load_songs_from_csv('dataset_top300.csv', n)

T = 1000
alpha = 0.999
T_min = 0.0001

times = []
for i in range(1):
    start = time.perf_counter()
    sa_playlist, sa_score = simulated_annealing(songs, max_duration, target_mood, T, alpha, T_min)
    end = time.perf_counter()
    times.append(end - start)
avg_time = sum(times) / len(times)

print("=============================== SIMULATED ANNEALING RESULT ================================")
print(f"Jumlah Dataset    : {n}")
print(f"Target Mood       : {target_mood}")
print(f"Batas Durasi      : {max_duration} menit")
print("===========================================================================================")
print(f"Suhu Awal (T0)    : {T}")
print(f"Cooling Rate      : {alpha}")
print(f"Suhu Minimum      : {T_min}")
print("===========================================================================================")
print(f"Skor Popularity   : {sa_score}")
print(f"Average Execution : {avg_time:.5}")
print("===========================================================================================")
print("Playlist Terbaik  :")
print("===========================================================================================")

total_duration = 0
for i, s in enumerate(sa_playlist, start=1):
    total_duration += s['duration']
    artist = s['artist'][:20] + '..' if len(s['artist']) > 20 else s['artist']
    name   = s['name'][:30]   + '..' if len(s['name'])   > 30 else s['name']
    print(f"{i:>2}. {artist:<22} | {name:<32} | {s['duration']:>4} mnt | {s['bpm']:>6.1f} BPM | {s['score']:>3}")

print("===========================================================================================")
print(f"Total Lagu        : {len(sa_playlist)}")
print(f"Total Durasi      : {round(total_duration, 2)} menit")
print("===========================================================================================")