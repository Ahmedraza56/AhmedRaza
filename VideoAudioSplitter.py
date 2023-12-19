from flask import Flask, render_template, request, send_file, Blueprint, send_from_directory
from moviepy.editor import VideoFileClip, AudioFileClip
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

VideoAudioSplitter_app = Blueprint("VideoAudioSplitter", __name__)
video_app = Flask(__name__)
video_app.config['UPLOAD_FOLDER'] = 'uploads'
video_app.config['OUTPUT_FOLDER'] = 'outputs'

# Ensure that the required directories exist
os.makedirs(video_app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(video_app.config['OUTPUT_FOLDER'], exist_ok=True)

@VideoAudioSplitter_app.route('/')
def index():
    return render_template('VideoAudioSplitter.html')

@VideoAudioSplitter_app.route('/', methods=['POST'])
def process_video():
    try:
        # Check if the post request has the file part
        if 'file' not in request.files:
            raise ValueError('No file part')

        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            raise ValueError('No selected file')

        # Save the uploaded file to disk
        video_path = os.path.join(video_app.config['UPLOAD_FOLDER'], 'uploaded_video.mp4')
        file.save(video_path)

        video = VideoFileClip(video_path)

        # Extract audio from the video
        audio = video.audio
        audio_filename = os.path.join(video_app.config['OUTPUT_FOLDER'], "temp.wav")
        audio.write_audiofile(audio_filename)

        # Load audio using PyDub
        audio = AudioSegment.from_wav(audio_filename)

        # Split audio on silence
        chunks = split_on_silence(audio, min_silence_len=1000, silence_thresh=-40)

        # Combine chunks back into a single audio segment
        combined = AudioSegment.empty()
        for chunk in chunks:
            combined += chunk

        # Save combined audio
        combined_filename = os.path.join(video_app.config['OUTPUT_FOLDER'], "combined.wav")
        combined.export(combined_filename, format="wav")

        # Save the processed video without audio
        processed_filename = os.path.join(video_app.config['OUTPUT_FOLDER'], "processed_video.mp4")
        video.write_videofile(processed_filename, codec='libx264', audio=False)

        return render_template('VideoAudioSplitter.html', audio='combined.wav', video='processed_video.mp4')

    except Exception as e:
        # Handle the exception (you can customize this part based on your needs)
        return render_template('VideoAudioSplitter.html', error=str(e))

@VideoAudioSplitter_app.route('/download/<filename>')
def download(filename):
    return send_from_directory(video_app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

# Add this route to remove the temporary audio file
@VideoAudioSplitter_app.route('/remove_temp_audio')
def remove_temp_audio():
    try:
        temp_audio_filename = os.path.join(video_app.config['OUTPUT_FOLDER'], "temp.wav")
        if os.path.exists(temp_audio_filename):
            os.remove(temp_audio_filename)
        return "Temporary audio file removed"
    except Exception as e:
        # Handle the exception (you can customize this part based on your needs)
        return f"Error: {str(e)}"


if __name__ == '__main__':
    video_app.register_blueprint(VideoAudioSplitter_app)
    video_app.run(debug=True)
