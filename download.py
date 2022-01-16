from __future__ import unicode_literals
import youtube_dl
import os 
import json
from azure.storage.blob import BlobServiceClient

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

def upload_file_to_storage(env,filepath,mood):
    connection_str = env["connection_string"]
    blob_service_client = BlobServiceClient.from_connection_string(connection_str)
    container_name = "songwav"
    filename = os.path.basename(filepath)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=os.path.join(mood,filename))
    print("[upload] Uploading " + filename + " to Azure Blob Storage")
    with open(filepath, "rb") as data:
        blob_client.upload_blob(data)
    print("[upload] Successfully uploaded " + filename + " to Azure Blob Storage")

def main():
    os.makedirs("song", exist_ok=True)
    moods = os.listdir("data")
    with open("env.json") as f:
        env = json.load(f)
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
                    upload_file_to_storage(env,os.path.join(path,track["title"]+".wav"),mood)
                except:
                    print("[error] Failed to download " + track["title"])
                    continue
            os.remove(os.path.join("data",mood,playlist_id))

if __name__ == "__main__":
    main()