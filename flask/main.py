import os
from flask import Flask, request, render_template, make_response, url_for
from video import validate_url, get_video_id, transcribe_video, validate_video_content
from recipe import create_recipe
from config import REDIS_HOST, REDIS_PORT, REQUEST_LIMIT, REQUEST_TIMEOUT_SECS
import redis

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

app = Flask(__name__)


@app.route("/")
def home_form():
    return render_template("home-form.html")


@app.route("/max-requests")
def max_requests():
    return render_template("rate-limit.html")


@app.route("/recipe", methods=["POST"])
def submit_video():
    url = request.form["video"]
    if validate_url(url):
        video_id = get_video_id(url)
        if not validate_video_content(video_id):
            return render_template("invalid-recipe.html")
        # Check if the user has exceeded the rate limit
        if not redis_client.exists(request.remote_addr):
            redis_client.set(request.remote_addr, 0)
            redis_client.expire(request.remote_addr, REQUEST_TIMEOUT_SECS)
        elif int(redis_client.get(request.remote_addr)) >= REQUEST_LIMIT:
            response = make_response("", 429)
            response.headers["HX-Redirect"] = url_for("max_requests")
            return response

        recipe = create_recipe(transcribe_video(video_id))
        redis_client.incr(request.remote_addr)
        return render_template("recipe.html", recipe=recipe)
    else:
        return ("", 204)


@app.route("/recipe/url", methods=["POST"])
def validate_video():
    url = request.form["video"]
    if not validate_url(url):
        return render_template("invalid-video.html", url=url)
    else:
        return render_template("valid-video.html", url=url)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
