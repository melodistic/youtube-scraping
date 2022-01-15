import json
from ytmusicapi import YTMusic
yt = YTMusic()
mood_list = yt.get_mood_categories()['Moods & moments']
with open("moods.json","w") as f:
    json.dump(mood_list,f)