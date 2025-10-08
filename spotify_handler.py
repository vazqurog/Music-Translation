import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = 'http://localhost:5000/callback'

# Initialize  spotify client
sp = None
try:
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        print("Warning: Spotify API credentials not found in .env file")
    else:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope='user-library-read user-read-private user-read-email'
        ))
except Exception as e:
    print(f"Error initializing Spotify client: {e}")

def get_track_info(song_name, artist_name):
    """Get track information including album artwork from Spotify"""
    if not sp:
        print("Spotify client not initialized, cannot get track info")
        return None
        
    try:
        # Search for the track
        results = sp.search(q=f'track:{song_name} artist:{artist_name}', type='track', limit=1)
        
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            return {
                'album_art': track['album']['images'][0]['url'],
                'album_name': track['album']['name'],
                'release_date': track['album']['release_date'],
                'spotify_url': track['external_urls']['spotify']
            }
        return None
    except Exception as e:
        print(f"Error getting track info: {e}")
        return None

def get_user_library():
    """Get user's saved tracks"""
    if not sp:
        print("Spotify client not initialized, cannot get user library")
        return []
        
    try:
        results = sp.current_user_saved_tracks()
        tracks = results['items']
        
        # Get more tracks if available
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
        
        # Format track information
        library = []
        for item in tracks:
            track = item['track']
            library.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album_art': track['album']['images'][0]['url'],
                'album_name': track['album']['name']
            })
        
        return library
    except Exception as e:
        print(f"Error getting user library: {e}")
        return [] 