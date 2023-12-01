from openai import OpenAI
import toml


client = OpenAI()

def assemble_prompt(video_text: str) -> list:
    with open('config.toml', 'r') as config_file:
        config = toml.load(config_file)
    return [
        {"role": "system", "content": config["prompts"]["role_prompt"]},
        {"role": "system", "content": config["prompts"]["instruction_prompt"]},
        {"role": "user", "content": f"""{video_text}"""}
    ]
    

def create_recipe(video_text: str):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=assemble_prompt(video_text)
    )
    return completion.choices[0].message.content


