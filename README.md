# Youtube Scraping

## About This Repository

This repository is a collection of scripts that I use to scrape data from Youtube Music. It can generate the json files that save in `data/<mood>/<playlist_id>.json` which contains the json data of track in the playlist.

The json data that already generate will use in the next steps which is download step that will download the video and postprocess the video into wav file and store in `song/<mood>` directory for using in model training.