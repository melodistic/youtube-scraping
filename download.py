from __future__ import unicode_literals
import youtube_dl
import os 
import json

def download_video(video_id, path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192'
        }],
        'postprocessor_args': [
            '-ar', '16000'
        ],
        'prefer_ffmpeg': False,
        'keepvideo': False,
        'outtmpl': os.path.join(path,'%(title)s.%(ext)s')
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v=' + video_id])

if __name__ == "__main__":
    os.makedirs("song", exist_ok=True)
    moods = os.listdir("data")
    for mood in moods:
        os.makedirs(os.path.join("song",mood), exist_ok=True)
        playlist = os.listdir(os.path.join("data",mood))
        for playlist_id in playlist:
            path = os.path.join("song",mood)
            with open(os.path.join("data",mood,playlist_id)) as f:
                tracks = json.load(f)
            for track in tracks:
                try:
                    download_video(track["id"],path)
                except:
                    continue