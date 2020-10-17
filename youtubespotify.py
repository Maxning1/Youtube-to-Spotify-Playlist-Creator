import json
import requests
import os

from secrets import spotify_user_id, spotify_token
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl

class CreatePlaylists:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token
        self.youtube_client = self.get_youtube_client
        self.all_song_info = {}

    #step 1: log into youtube
    def get_youtube_client(self):
        #copied from youtube api
        #disable oauthlib's https verification when running locally
        # DO NOT leave this option enabled in production

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secrets.json"

        #get credentials and make an api client
        scopes = "[https://www.googleapis.com/auth/youtube/youtube.readonly]"
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        credentials = flow.run_console()

        #from Youtube data api
        youtube_client = googleapiclient.discovery.build(api_service_name, api_version, credentials = credentials)
        return youtube_client

    #step 2: grab our liked video and create dictionary of important song info
    def get_liked_videos(self):
        request = self.youtube_client.videos().list(
            part = "snippet,content Details,Statistics",
            myRating = "like"
        )
        response = request.execute()
        #collect each video and get important info
        for item in response["items"]:
            video_title = items["snippet"]["title"]
            youtube_url = "https://www.youtube.com/watch?={}".format(item["id"])
        
            #use youtube_dl to collect song name and artist
            video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download = False)
            song_name = video["track"]
            artist = video["artist"]
            
            #save all important info
            self.all_song_info[video_title] = {
                "youtube_url": youtube_url,
                "song_name": song_name,
                "artist": aristt,

                #add the uri, easy to get song to put into playlist
                "spotify_uri": self.get_spotify_uri(song_name, artist)
            }
    #step 3: create new playlist
    def create_playlist(self):
        request_body = json.dumps({
            "name": "Liked Youtube Vids",
            "description": "All Liked Youtube Videos",
            "public": True
        })

        query = "https://api.spotify.com/v1/users/{user_id}/playlists".format(self.user_id)
        response = requests.post(
            query,
            data = response_body,
            headers = {
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        #playlist id
        return response_json("id")
    def get_spotify_uri(self, song_name, artist):
        query = "https://api.spotify.com/v1/users/{user_id}/playlists".format(
            song_name,
            artist
        )
        response = request.get(
            query,
            headers = {
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]
        #only use the first song
        uri = songs[0]["uri"]
        return uri
    def add_song_to_playlist(self):
        #populate our song dictionary
        self.get_liked_videos
        #collect all of our uri
        uri = []
        for song,info in self.all_song_info.items():
            uri.append(["spotify_uri"])
        #create a new playlist
        playlist_id = self.create_playlist()
        #add all songs into playlist
        request_data = json.dumps(uris)

        query = "https://api.spotify.com/v1/users/{user_id}/playlists"
        response = requests.post(
            query,
            data = request_data,
            headers = {
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json()
        return response_json
