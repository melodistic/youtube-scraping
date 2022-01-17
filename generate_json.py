import json
import os
from ytmusicapi import YTMusic
from langdetect import detect
yt = YTMusic()

def get_playlist_by_param(param):
    playlist = yt.get_mood_playlists(param)
    return playlist

def get_tracks(param):
    track = yt.get_playlist(param)["tracks"]
    data = []
    for i in track:
        try:
            if detect(i["title"]) == "en":
                data.append({"id": i["videoId"], "title": i["title"]})
        except:
            continue
    return data

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    mood_list = yt.get_mood_categories()['Moods & moments']
    valid_moods = ["Chill", "Feel Good", "Romance", "Focus", "Sleep", "Energy Boosters", "Party", "Workout"]
    for i in mood_list:
        if i["title"] in valid_moods:
            os.makedirs(os.path.join("data",i["title"]), exist_ok=True)
            playlist = get_playlist_by_param(i["params"])
            for j in playlist[:10]:
                tracks = get_tracks(j["playlistId"])
                with open(os.path.join("data",i["title"],j["playlistId"] + ".json"),"w") as f:
                    json.dump(tracks,f)