import os
from flask import Flask, request, render_template
from transcribe import validate_video, get_video_id, transcribe_video
from recipe import create_recipe

app = Flask(__name__)

@app.route('/')
def home_form():
    return render_template('home-form.html')

@app.route('/recipe', methods=['POST'])
def submit_video():
    url = request.form['video']
    if validate_video(url):
        video_id = get_video_id(url)
        recipe_html = create_recipe(transcribe_video(video_id))
        return render_template('recipe.html', recipe_html=recipe_html)
    else:
        return ('', 204)


@app.route('/recipe/url', methods=['POST'])
def validate_url():
    url = request.form['video']
    if not validate_video(url):
         return render_template('invalid-video.html', url=url)
    else:
        return render_template('valid-video.html', url=url)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))