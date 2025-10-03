import yt_dlp

playlist_url = 'https://www.youtube.com/watch?v=8fM1xnLTApg'  
save_path = 'youtube_download/' 

def download_best_audio_as_mp3(video_url, save_path=save_path):
    ydl_opts = {
        'format': 'bestaudio/best', 
        'outtmpl': save_path + '/%(title)s.%(ext)s',  # Save path and file name
        'postprocessors': [{  # Post-process to convert to MP3
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Convert to mp3
            'preferredquality': '0',  # '0' means best quality, auto-determined by source
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        
def download_best_audio_as_mp4(video_url, save_path=save_path):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best', 
        'outtmpl': save_path + '/%(title)s.%(ext)s',  # Save path and file name
        'merge_output_format': 'mp4',  # Ensure the output format is mp4
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        
def download_best_audio_quality(video_url, save_path=save_path):
    """
    Downloads audio-only in the highest quality format (opus/webm).
    Maintains original format without transcoding to preserve quality.
    """
    ydl_opts = {
        'format': '140/bestaudio/best',  # Prioritize format 251 (opus/webm), fall back to best audio
        'outtmpl': save_path + '/%(title)s.%(ext)s',  # Save path and file name
        'ignoreerrors': True, 
        'download_archive': 'archive.txt',  # Track downloaded videos
        # No post-processors to avoid quality loss from transcoding
        'postprocessors': [{
            'key': 'FFmpegMetadata',  # Only add metadata, no audio conversion
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])        

if __name__ == "__main__":
    # Replace with your playlist URL
    # download_best_audio_as_mp3(playlist_url, save_path)
    # download_best_audio_as_mp4(playlist_url, save_path)
    download_best_audio_quality(playlist_url, save_path)