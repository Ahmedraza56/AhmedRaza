from flask import Flask, render_template, request
from gtts import gTTS
from io import BytesIO
import base64

app = Flask(__name__)

# Function to convert text to speech
def text_to_speech(text):
    try:
        tts = gTTS(text)
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer
    except Exception as e:
        # Handle the exception (you can log it, display an error message, etc.)
        print(f"Error in text_to_speech: {str(e)}")
        return None

# Function to set download link for audio file
def get_audio_download_link(buffer, filename="audio.mp3"):
    try:
        buffer.seek(0)
        b64_data = base64.b64encode(buffer.read()).decode()
        return f'data:audio/mp3;base64,{b64_data}'
    except Exception as e:
        # Handle the exception (you can log it, display an error message, etc.)
        print(f"Error in get_audio_download_link: {str(e)}")
        return None

# Index route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input_text = request.form.get('user_input_text')
        if user_input_text:
            try:
                # Call function to convert text to speech
                audio_buffer = text_to_speech(user_input_text)
                if audio_buffer:
                    download_link = get_audio_download_link(audio_buffer)
                    return render_template('text_to_speech.html', audio_link=download_link)
                else:
                    # Handle the case where audio conversion failed
                    return render_template('text_to_speech.html', audio_link=None, error_message="Audio conversion failed.")
            except Exception as e:
                # Handle the exception (you can log it, display an error message, etc.)
                print(f"Error in index route: {str(e)}")
                return render_template('text_to_speech.html', audio_link=None, error_message="An error occurred.")
    
    return render_template('text_to_speech.html', audio_link=None, error_message=None)

if __name__ == '__main__':
    app.run(debug=True)
