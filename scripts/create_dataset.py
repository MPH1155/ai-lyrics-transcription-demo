import os
import pandas as pd

def create_dataset(audio_dir, lyrics_dir, output_csv):
    data = []
    audio_files = [f for f in os.listdir(audio_dir) if f.endswith(('.mp3', '.wav'))]
    
    for audio_file in audio_files:
        base_name = os.path.splitext(audio_file)[0]
        lyrics_file = f"{base_name}.txt"
        lyrics_path = os.path.join(lyrics_dir, lyrics_file)
        audio_path = os.path.join(audio_dir, audio_file)
        
        if os.path.exists(lyrics_path):
            with open(lyrics_path, 'r', encoding='utf-8') as f:
                lyrics = f.read().strip()
            data.append({'audio': audio_path, 'lyrics': lyrics})
        else:
            print(f"Warning: Lyrics file for {audio_file} not found.")

    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print(f"Dataset CSV created at {output_csv}")


audio_directory = "original_data/youtube_audio/"
lyrics_directory = "original_data/lyrics/"
output_csv = "original_data/dataset.csv"

create_dataset(audio_directory, lyrics_directory, output_csv)