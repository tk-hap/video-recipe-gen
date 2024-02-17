from openai import OpenAI
from pydantic import BaseModel
import toml
import instructor 
from models import RecipeDetails

#TODO: Could use langchain summarization to create recipes from longer transcriptions.

client = instructor.patch(OpenAI())

def assemble_prompt(video_text: str) -> list:
    with open('config.toml', 'r') as config_file:
        config = toml.load(config_file)
    return [
        {"role": "system", "content": config["prompts"]["role_prompt"]},
        {"role": "system", "content": config["prompts"]["instruction_prompt"]},
        {"role": "user", "content": f"""{video_text}"""}
    ]
    

def create_recipe(video_text: str):
    recipe_details = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        temperature=0.2,
        response_model=RecipeDetails,
        messages=assemble_prompt(video_text)
    )
    assert isinstance(recipe_details, RecipeDetails)
    #print(recipe.title, recipe.ingredients, recipe.instructions, recipe.notes)
    return recipe_details 



