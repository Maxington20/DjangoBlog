from django.core.management.base import BaseCommand
from blog.models import Post, Image
import openai
import requests
from requests_oauthlib import OAuth2Session
from maxs_blog.credentials import ACCESS_TOKEN, API_KEY 

# Fetch image function
def fetch_images(description, access_token, count=5):
    oauth = OAuth2Session(token={"access_token": access_token, "token_type": "Bearer"})
    response = oauth.get(f"https://api.unsplash.com/search/photos?query={description}&per_page={count}")

    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])
        image_data = [{"url": result["urls"]["small"], "description": result["description"]} for result in results]
        return image_data
    return []

class Command(BaseCommand):
    help = "Generate a blog post using GPT-4 and Unsplash API"

    def handle(self, *args, **options):
        title = input("Enter the blog post title: ")

        image_description = input("Enter the image description: ")

        # GPT-4 API
        openai.api_key = API_KEY
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Write a detailed blog post about {title}. It must be at least 500 words long and not repetitive.",
            max_tokens=3000,
            n=1,
            stop=None,
            temperature=0.7,
        )
        content = response.choices[0].text.strip()

        
        #description = response.choices[0].text.strip()  # Use the generated content as description
        image_data = fetch_images(image_description, ACCESS_TOKEN, count=5)
        # Create a new post
        new_post = Post(title=title, content=content)
        new_post.save()

        # Add images to the post
        for data in image_data:
            print(image_data)
            image = Image(url=data["url"], description=data["description"], post=new_post)
            image.save()

        self.stdout.write(self.style.SUCCESS("Successfully generated a blog post."))