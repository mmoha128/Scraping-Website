import requests
from bs4 import BeautifulSoup
import time

BASE_URL = 'https://www.gulte.com'

def get_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Failed to retrieve content from {url}. Status code: {response.status_code}")
        return None

def extract_movie_review_links():
    page = 1
    all_links = []

    while True:
        url = f'{BASE_URL}/moviereviews/page/{page}/'
        print(f"Fetching: {url}")
        soup = get_soup(url)

        if not soup:
            print("No content found. Ending.")
            break

        post_thumbnails = soup.find_all('div', class_='post-thumbnail')
        if not post_thumbnails:
            print("No more reviews found. Stopping pagination.")
            break

        page_links = []
        for thumbnail in post_thumbnails:
            link_tag = thumbnail.find('a', href=True)
            if link_tag:
                page_links.append(link_tag['href'])

        print(f"Page {page}: Found {len(page_links)} links.")
        all_links.extend(page_links)
        page += 1
        time.sleep(1)

    return all_links


def extract_rating_gulte(soup):
    # Step 1: Find the <strong> tag containing "Rating:"
    rating_tag = soup.find('strong', string=lambda x: x and 'Rating' in x)
    if rating_tag:
        rating_text = rating_tag.text.split(" ")[-1].strip()  
        return rating_text.split("/")[0]
    return None

def scrape_movie_details(url):
    soup = get_soup(url)
    if soup:
        # Extract the movie name from the URL
        movie_name = url.split('/')[-1].replace('-', ' ').title()

        # Extract the rating using the extract_rating_gulte function
        rating = extract_rating_gulte(soup)
        if not rating:
            rating = 'No Rating Found'

        return {
            'movie_name': movie_name,
            'rating': rating,
            'url': url
        }
    return None