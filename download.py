from __future__ import unicode_literals
import json
import os 
import time
from azure.storage.blob import BlobServiceClient
from yt_dlp import YoutubeDL

def download_video(video_id, path):
    ydl_opts = {
        'format': 'bestaudio',
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
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v=' + video_id])

def upload_file_to_storage(blob_service_client,filepath,mood):
    container_name = "songwav"
    filename = os.path.basename(filepath)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=os.path.join(mood,filename))
    print("[upload] Uploading " + filename + " to Azure Blob Storage")
    with open(filepath, "rb") as data:
        blob_client.upload_blob(data)
    print("[upload] Successfully uploaded " + filename + " to Azure Blob Storage")
    os.remove(filepath)

def main():
    os.makedirs("song", exist_ok=True)
    moods = os.listdir("data")
    with open("env.json") as f:
        env = json.load(f)
    connection_str = env["connection_string"]
    print("[connect] Connecting to Azure Blob Storage")
    blob_service_client = BlobServiceClient.from_connection_string(connection_str)
    time.sleep(10)
    print("[connect] Successfully connected to Azure Blob Storage")
    for mood in moods:
        count = 0
        os.makedirs(os.path.join("song",mood), exist_ok=True)
        playlist = os.listdir(os.path.join("data",mood))
        for playlist_id in playlist:
            path = os.path.join("song",mood)
            with open(os.path.join("data",mood,playlist_id)) as f:
                tracks = json.load(f)
            for track in tracks:
                try:
                    download_video(track["id"],path)
                    upload_file_to_storage(blob_service_client,os.path.join(path,track["title"]+".wav"),mood)
                    count += 1
                    if count == 100:
                        break
                except:
                    print("[error] Failed to download " + track["title"])
                    try:
                        os.remove(os.path.join(path,track["title"]+".wav"))
                    except OSError:
                        pass  
                    continue
            os.remove(os.path.join("data",mood,playlist_id))
            if count == 100:
                break

if __name__ == "__main__":
    main()