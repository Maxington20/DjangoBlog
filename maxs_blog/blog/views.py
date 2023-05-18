from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post
import openai
import requests
from requests_oauthlib import OAuth2Session

def index(request):
    latest_posts = Post.objects.order_by('-pub_date')
    print(f"Number of posts: {len(latest_posts)}")
    for post in latest_posts:
        print(f"Post title: {post.title}")
    context = {'latest_posts': latest_posts}
    return render(request, 'blog/index.html', context)

def fetch_image(query, access_token):
    client_id = "Dlh3b8S-WbiC0ylywlXOzsOGVAxKmdZxi7QYv6JJWuM"
    client_secret = "383OuzINE4JkcJ5Xvx92ubBqLwYuQnCVY0RMlFZ9-G8"
    url = f"https://api.unsplash.com/search/photos?page=1&query={query}"

    headers = {
        "Accept-Version": "v1",
        "Authorization": f"Bearer {access_token}"
    }

    oauth = OAuth2Session(client_id, token={"access_token": access_token, "token_type": "Bearer"})

    response = oauth.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data['results']:
            image_url = data['results'][0]['urls']['small']
            return image_url
    else:
        print(f"Error: {response.status_code}")
        return None

def generate_post(request=None, title=None):
    if request is None and title is None:
        return

    if request is not None and request.method == 'POST':
        title = request.POST['title']

    prompt = f"Write a blog post about {title} with relevant images"

    # GPT-4 API
    openai.api_key = "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"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1500,
        n=1,
        stop=None,
        temperature=0.7,
    )
    content = response.choices[0].text.strip()

    # Unsplash API with OAuth2
    access_token = "your_unsplash_access_token"
    image_url = fetch_image(title, access_token)

    # Create a new post
    new_post = Post(title=title, content=content, image_url=image_url)
    new_post.save()

    if request is not None:
        # Redirect to the index page
        return HttpResponseRedirect(reverse('blog:index'))

    return