import json
import sys
from ytmusicapi import YTMusic
yt = YTMusic()
def get_track(param):
    track = yt.get_playlist(param)["tracks"]
    data = []
    for i in track:
        data.append({"id": i["videoId"], "title": i["title"]})
    return data

if __name__ == "__main__":
    if len(sys.argv) > 1:
        param = sys.argv[1]
        track = get_track(param)
        with open(param + ".json","w") as f:
            json.dump(track,f)
    else:
        print("Usage: get_track.py <param>")