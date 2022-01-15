import json
import sys
from ytmusicapi import YTMusic
yt = YTMusic()

def get_playlist_by_param(param):
    playlist = yt.get_mood_playlists(param)
    return playlist

if __name__ == "__main__":
    if len(sys.argv) > 1:
        param = sys.argv[1]
        playlist = get_playlist_by_param(param)
        with open(param + ".json","w") as f:
            json.dump(playlist,f)
    else:
        print("Usage: get_playlist.py <param>")