import os
from flask import Flask, request, render_template, make_response, url_for
from transcribe import validate_url, get_video_id, transcribe_video
from recipe import create_recipe
import redis

redis_host = os.environ.get("REDISHOST", "localhost")
redis_port = int(os.environ.get("REDISPORT", 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port)

request_limit = int(os.environ.get("REQUEST_LIMIT", 3))
request_timeout_secs = int(os.environ.get("REQUEST_TIMEOUT_SECS", 60))

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
        # Check if the user has exceeded the rate limit
        if not redis_client.exists(request.remote_addr):
            redis_client.set(request.remote_addr, 0)
            redis_client.expire(request.remote_addr, request_timeout_secs)
        elif int(redis_client.get(request.remote_addr)) >= request_limit:
            resp = make_response("", 429)
            resp.headers["HX-Redirect"] = url_for("max_requests")
            return resp

        recipe = create_recipe(transcribe_video(video_id))
        redis_client.incr(request.remote_addr)
        return render_template("recipe.html", recipe=recipe)
    else:
        return ("", 204)


@app.route("/recipe/url", methods=["POST"])
def validate_url():
    url = request.form["video"]
    if not validate_url(url):
        return render_template("invalid-video.html", url=url)
    else:
        return render_template("valid-video.html", url=url)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
