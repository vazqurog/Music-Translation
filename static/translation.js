document.addEventListener('DOMContentLoaded', async function() {
    const originalElement = document.getElementById('original-lyrics');
    const translatedElement = document.getElementById('translated-lyrics');
    const songInfoContainer = document.getElementById('song-info');

    if (!originalElement || !translatedElement) {
        console.error("Could not find lyrics elements");
        return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const lyrics = urlParams.get('lyrics');
    const targetLang = urlParams.get('lang') || 'EN-US';
    
    // Get song info from URL if available
    const songName = urlParams.get('song');
    const artistName = urlParams.get('artist');
    const albumArt = urlParams.get('album_art');
    const albumName = urlParams.get('album_name');

    // Display song info if available
    if (songName && artistName) {
        let songInfoHTML = '';
        
        if (albumArt) {
            songInfoHTML += `<img src="${albumArt}" alt="${songName}" class="album-art">`;
        }
        
        songInfoHTML += `
            <div class="song-details">
                <div class="song-title">${songName}</div>
                <div class="song-artist">${artistName}</div>
                ${albumName ? `<div class="song-album">${albumName}</div>` : ''}
            </div>
        `;
        
        songInfoContainer.innerHTML = songInfoHTML;
    }

    if (!lyrics) {
        originalElement.textContent = 'No lyrics provided';
        translatedElement.textContent = 'No lyrics to translate';
        return;
    }

    // Display original lyrics immediately
    originalElement.textContent = lyrics;
    translatedElement.textContent = 'Translating...';

    try {
        // Request translation
        const response = await fetch('/api/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                lyrics: lyrics,
                lang: targetLang
            })
        });

        if (!response.ok) {
            throw new Error('Translation request failed');
        }

        const data = await response.json();
        if (data.translated_lyrics) {
            translatedElement.textContent = data.translated_lyrics;
        } else {
            translatedElement.textContent = 'Translation failed';
        }
    } catch (error) {
        console.error('Error:', error);
        translatedElement.textContent = 'Error during translation';
    }
});