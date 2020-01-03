import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models

BASE_URL = "https://newyork.craigslist.org/search/?query=%s"
BASE_IMAGE_URL = "https://images.craigslist.org/%s_300x300.jpg"

# Create your views here.
def home(request):
    return render(request, template_name='base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_URL % quote_plus(search)

    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_listings = soup.find_all('li', {'class': 'result-row'})

    parsed_post_listings = []
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = "N/A"


        if post.find(class_= 'result-image').get('data-ids'):
            post_image = post.find(class_= 'result-image').get('data-ids').split(",")[0].split(":")[1]
            post_image_url = BASE_IMAGE_URL % post_image
        else:
            post_image_url = "https://developer.rhino3d.com/images/rhinopython-guides-col1.png"

        parsed_post_listings.append((post_title, post_url, post_price, post_image_url))

    stuff_for_frontend = {
        'search': search,
        'parsed_post_listings': parsed_post_listings
    }
    return render(request, template_name='my_app/new_search.html', context=stuff_for_frontend)
