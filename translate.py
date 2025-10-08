import deepl
import os 
from dotenv import load_dotenv
load_dotenv()

translator = deepl.Translator(os.getenv('DEEP_L_AUTH_KEY'))

def translate_lyrics(lyrics, lang):
    if not lyrics:
        return "Error: No lyrics provided for translation."
    if not lang:
        return "Error: No target language specified."
    
    # Split lyrics into lines
    lines = lyrics.split('\n')
    
    # Translate each line separately to preserve structure
    translated_lines = []
    for line in lines:
        if line.strip():  # Only translate non-empty lines
            translated = translator.translate_text(line, target_lang=lang).text
            translated_lines.append(translated)
        else:
            translated_lines.append('')  # Preserve empty lines
    
    # Join the lines back together
    return '\n'.join(translated_lines)
        


