from openai import OpenAI
import toml
import instructor
import structlog
from models import RecipeDetails

# TODO: Could use langchain summarization to create recipes from longer transcriptions.

logger = structlog.get_logger()

client = instructor.patch(OpenAI())


def assemble_prompt(video_text: str) -> list:
    with open("config.toml", "r") as config_file:
        config = toml.load(config_file)
    return [
        {"role": "system", "content": config["prompts"]["role_prompt"]},
        {"role": "system", "content": config["prompts"]["instruction_prompt"]},
        {"role": "user", "content": f"""{video_text}"""},
    ]


def create_recipe(video_text: str):
    recipe_details = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        max_retries=3,  # If pydantic validation fails, model will be reprompted
        temperature=0.2,
        response_model=RecipeDetails,
        messages=assemble_prompt(video_text),
    )
    return recipe_details
