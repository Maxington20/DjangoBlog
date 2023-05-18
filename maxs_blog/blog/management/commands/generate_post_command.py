from django.core.management.base import BaseCommand
from blog.models import Post
import openai
import requests
from requests_oauthlib import OAuth2Session

# Fetch image function
def fetch_image(query, access_token):
    oauth = OAuth2Session(token={"access_token": access_token, "token_type": "Bearer"})
    response = oauth.get(f"https://api.unsplash.com/search/photos?query={query}&per_page=1")

    if response.status_code == 200:
        data = response.json()
        if len(data["results"]) > 0:
            return data["results"][0]["urls"]["small"]
    return None

class Command(BaseCommand):
    help = "Generate a blog post using GPT-4 and Unsplash API"

    def handle(self, *args, **options):
        title = input("Enter the blog post title: ")

        # GPT-4 API
        openai.api_key = "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"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Write a blog post about {title} with relevant images",
            max_tokens=1500,
            n=1,
            stop=None,
            temperature=0.7,
        )
        content = response.choices[0].text.strip()

        # Unsplash API with OAuth2
        access_token = "lHr7AT2hT19cbcyIbW_c5kX3PwADHA_QGqczZA1bp6I"
        image_url = fetch_image(title, access_token)

        # Create a new post
        new_post = Post(title=title, content=content, image_url=image_url)
        new_post.save()

        self.stdout.write(self.style.SUCCESS("Successfully generated a blog post."))