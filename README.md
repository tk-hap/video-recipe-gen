# YouTube video to Recipe
Transcribes a YouTube video sends the transcript to OpenAi to summarize as a recipe.


## Design
Intend to keep this as simple as possible.
Using a Flask backend and plain html on the front end.

### Backend
- Flask
- Redis

### Frontend
- Pico CSS
- HTMX



### Notes:
- Should limit the number of requests by setting a limit of 5 requests per user, per day.
    - This can be done by using the IP address of the user.
    - This can be done by using a cookie.

### Commands:
- `docker run --name my-redis -d -p 6379:6379 redis`
-