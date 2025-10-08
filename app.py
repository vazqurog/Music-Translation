from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from translate import translate_lyrics
from lyrics import search_lyrics
from spotify_handler import get_track_info, get_user_library
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key')

def add_security_headers(response):
    """Add security headers to response"""
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "style-src 'self' https://fonts.googleapis.com 'unsafe-inline'; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: https://i.scdn.co; "  # Allow Spotify image URLs
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
        "connect-src 'self'"
    )
    return response

@app.after_request
def after_request(response):
    return add_security_headers(response)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search_page():
    return render_template('search.html')

@app.route('/translate')
def translate_page():
    return render_template('translation.html')

@app.route('/library')
def library_page():
    return render_template('library.html')

@app.route('/callback')
def spotify_callback():
    return redirect(url_for('library_page'))

@app.route('/api/search', methods=['POST'])
def search_lyrics_route():
    data = request.json
    song_name = data.get('song')
    artist_name = data.get('artist')

    if not song_name or not artist_name:
        return jsonify({'error': 'Please provide artist and song'}), 400
    
    # Get lyrics
    lyrics = search_lyrics(song_name, artist_name)
    
    # Get Spotify track info
    track_info = get_track_info(song_name, artist_name)
    
    return jsonify({
        'lyrics': lyrics,
        'track_info': track_info
    })

@app.route('/api/translate', methods=['POST'])
def translate_lyrics_route():
    data = request.json
    lyrics = data.get('lyrics')
    lang = data.get('lang', 'EN-US')

    if not lyrics:
        return jsonify({'error': 'Missing lyrics'}), 400

    return jsonify({"translated_lyrics": translate_lyrics(lyrics, lang)})

@app.route('/api/library', methods=['GET'])
def get_library_route():
    try:
        library = get_user_library()
        return jsonify({'library': library})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)