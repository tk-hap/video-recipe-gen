# YouTube Video to Recipe Generator

This application transcribes a YouTube cooking video and uses OpenAI's GPT-3 model to summarize the transcript into a recipe.

Try it at https://videorecipegen.com/

## Features

- Transcribes YouTube cooking videos into text.
- Summarizes the transcription into a recipe using OpenAI's GPT-3 model.
- Formats the response into a recipe card.
- Limits the number of requests per user to prevent abuse.

## Technologies Used

### Backend
- Flask: Used to serve the application. 
- Redis: Used to store the number of requests per user. 

### Frontend
- Pico CSS: A minimalistic CSS framework.
- HTMX: Used to provide dynamic HTML content.

## Local installation

1. Clone the repository.
2. Install the dependencies with `pip install -r requirements.txt`.
3. Run a redis docker container with `docker run --name my-redis -d -p 6379:6379`.
3. Create a .env file with your `OPENAI_API_KEY` and `YOUTUBE_API_KEY` values, you may also optionally set environment variables for the Redis, request limit and max video length settings.
4. Run the application from the /flask directory with `flask --app main run`.

## Usage

1. Submit a YouTube cooking video URL.
2. The application will transcribe the video and generate a recipe.
3. If the video is not a cooking video or is greater than the `MAX_VIDEO_DURATION`, an error message will be displayed.

## Limitations

- The application limits the number of requests to 5 per user per day. This is done using the IP address of the user.
- The application limits the duration of the video to 45 minutes. This is to prevent inputs greater than the models max tokens.
- The accuracy of the recipe depends on the quality of the video transcription and the performance of the GPT-3 model.