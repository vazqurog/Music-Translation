// Utility functions
function displayLyrics() {
    const originalElement = document.getElementById('original-lyrics');
    const translatedElement = document.getElementById('translated-lyrics');
    
    if (originalElement && translatedElement) {
        const originalLyrics = sessionStorage.getItem('originalLyrics');
        const translatedLyrics = sessionStorage.getItem('translatedLyrics');
        
        originalElement.textContent = originalLyrics || 'No lyrics available';
        translatedElement.textContent = translatedLyrics || 'No translation available';
        
        if (originalLyrics && translatedLyrics) {
            sessionStorage.removeItem('originalLyrics');
            sessionStorage.removeItem('translatedLyrics');
        }
    }
}

async function fetchLyrics() {
    const artist = document.getElementById("artist").value;
    const song = document.getElementById("song").value;
    const language = document.getElementById("language").value;
    const statusMessage = document.getElementById("status-message");
    const albumArtContainer = document.getElementById("album-art-container");

    if (!artist || !song) {
        statusMessage.textContent = "Please enter both artist and song name.";
        return;
    }

    try {
        statusMessage.textContent = "Searching for lyrics...";
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ song, artist })
        });

        const data = await response.json();
        
        if (!data.lyrics) {
            statusMessage.textContent = "Lyrics not found.";
            return;
        }

        // Display album artwork if available
        if (data.track_info && data.track_info.album_art) {
            albumArtContainer.innerHTML = `<img src="${data.track_info.album_art}" alt="${song}" class="album-art">`;
        } else {
            albumArtContainer.innerHTML = '';
        }

        // Prepare URL parameters for translation page
        const params = new URLSearchParams({
            lyrics: data.lyrics,
            lang: language,
            song: song,
            artist: artist
        });
        
        // Add album info if available
        if (data.track_info) {
            if (data.track_info.album_art) params.append('album_art', data.track_info.album_art);
            if (data.track_info.album_name) params.append('album_name', data.track_info.album_name);
        }
        
        window.location.href = `/translate?${params.toString()}`;
    } catch (error) {
        console.error("Error:", error);
        statusMessage.textContent = "An error occurred while processing your request.";
    }
}

// Event listeners
document.addEventListener("DOMContentLoaded", function() {
    // For translation page
    if (document.getElementById('original-lyrics')) {
        displayLyrics();
    }
    
    // For search page
    const translateButton = document.getElementById("translate-btn");
    if (translateButton) {
        translateButton.addEventListener("click", fetchLyrics);
    }
    
    // For home page
    const enterButton = document.querySelector(".button");
    if (enterButton) {
        enterButton.addEventListener("click", function() {
            window.location.href = "/search";
        });
    }

    // Check for URL parameters to pre-fill search
    const urlParams = new URLSearchParams(window.location.search);
    const song = urlParams.get('song');
    const artist = urlParams.get('artist');
    
    if (song && artist) {
        document.getElementById('song').value = song;
        document.getElementById('artist').value = artist;
        fetchLyrics();
    }
});