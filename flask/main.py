from flask import Flask, request, render_template
from transcribe import transcribe_video
from recipe import create_recipe

app = Flask(__name__)

@app.route('/')
def home_form():
    return render_template('home-form.html')

@app.route('/', methods=['POST'])
def submit_video():
    video_id = request.form['video']
    return create_recipe(transcribe_video(video_id))