import os 
from lyricsgenius import Genius
from dotenv import load_dotenv
load_dotenv()

# Initialize the Genius API
genius = Genius(os.getenv("GENIUS_CLIENT_TOKEN"))
genius.verbose = False
genius.remove_section_headers = True

def search_lyrics(song, artist):
    try:
        if song and artist:
            song_data = genius.search_song(song, artist)
            if song_data and song_data.lyrics:
                print("DEBUG: Lyrics received:", song_data.lyrics)
                lyrics = song_data.lyrics
                lines = [line.strip() for line in lyrics.split('\n') if line.strip()]  
                lines = [line for line in lines if not any(meta in line.lower() 
                    for meta in ['contributors', 'embed', 'you might also like'])]
                
                
                n = len(lines)
                for i in range(n//2):  
                    sequence = lines[i:i+4]  
                    if len(sequence) < 4:
                        continue
                    
                    for j in range(i + len(sequence), n - len(sequence) + 1):
                        if lines[j:j+4] == sequence:
                            # repeat point
                            return '\n'.join(lines[:j])
                
                return '\n'.join(lines)
            else:
                return "Error: No lyrics found for this song."
    except Exception as e:
        return f"Search Lyrics Error: {e}"