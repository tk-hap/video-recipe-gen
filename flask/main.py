from flask import Flask, request, render_template
from transcribe import get_video_id, transcribe_video
from recipe import create_recipe

app = Flask(__name__)

@app.route('/')
def home_form():
    return render_template('home-form.html')

@app.route('/recipe', methods=['POST'])
def submit_video():
    url = request.form['video']
    try:
        video_id = get_video_id(url)
    except IndexError:
        return "Error"
    recipe_html = create_recipe(transcribe_video(video_id))
    return render_template('recipe.html', recipe_html=recipe_html)
