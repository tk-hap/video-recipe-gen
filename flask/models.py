from pydantic import BaseModel
from weasyprint import HTML
from io import BytesIO
import jinja2


class RecipeDetails(BaseModel):
    title: str
    ingredients: list
    instructions: list
    notes: str = ""


class RecipeGenerator:
    def __init__(self, details: RecipeDetails, video_id: str):
        self.details = details
        self.video_id = video_id
        self.html_recipe = None
        self.pdf_recipe = None

    def generate_html(self) -> str:
        self.html_recipe = (
            jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
            .get_template("base-recipe.html")
            .render(recipe=self.details)
        )
        return self.html_recipe

    def generate_pdf(self) -> BytesIO:
        self.pdf_recipe = BytesIO(
            HTML(string=self.html_recipe).write_pdf(
                stylesheets=[
                    "https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css"
                ]
            )
        )
        return self.pdf_recipe
