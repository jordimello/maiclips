from flask import Flask, render_template, request, jsonify
import whisper
import os
import tempfile
from moviepy.editor import VideoFileClip

app = Flask(__name__)

OPENAI_API_KEY = "PLACEHOLDER"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['video']
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    file.save(tmp.name)
    model = whisper.load_model("base")
    result = model.transcribe(tmp.name)
    clips = []
    video = VideoFileClip(tmp.name)
    for i, segment in enumerate(result['segments'][:3]):
        start = max(0, segment['start'] - 1)
        end = min(video.duration, segment['end'] + 1)
        clip_path = f"clip_{i}.mp4"
        video.subclip(start, end).write_videofile(clip_path, logger=None)
        clips.append(clip_path)
    return jsonify({"clips": clips, "transcript": result['text']})

if __name__ == '__main__':
    app.run(debug=True)
