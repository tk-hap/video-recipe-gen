from openai import OpenAI
client = OpenAI()


def create_recipe(video_text):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an experienced food writer, skilled at writing accurate recipes.",
            },
            {
                "role": "user",
                "content": f"You will be provided with a transcript of a cooking video (delimited with XML tags). Please summarize the transcript to create a recipe. Please be accurate to the transcript. Return the recipe in html starting with a list of the required and optional ingredients followed by the directions to make the dish. The video transcript is delimited by triple quotes. <recipe>{video_text}</recipe>",
            },
        ],
    )
    return completion.choices[0].message.content


