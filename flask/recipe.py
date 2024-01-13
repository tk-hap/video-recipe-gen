from openai import OpenAI
from pydantic import BaseModel
import toml
import instructor 


client = instructor.patch(OpenAI())

class RecipeDetails(BaseModel):
    title: str
    ingredients: list
    instructions: list
    notes: str = ''


def assemble_prompt(video_text: str) -> list:
    with open('config.toml', 'r') as config_file:
        config = toml.load(config_file)
    return [
        {"role": "system", "content": config["prompts"]["role_prompt"]},
        {"role": "system", "content": config["prompts"]["instruction_prompt"]},
        {"role": "user", "content": f"""{video_text}"""}
    ]
    

def create_recipe(video_text: str):
    recipe = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.2,
        response_model=RecipeDetails,
        messages=assemble_prompt(video_text)
    )
    assert isinstance(recipe, RecipeDetails)
    #print(recipe.title, recipe.ingredients, recipe.instructions, recipe.notes)
    return recipe 


