import requests
from bs4 import BeautifulSoup

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
    soup = get_soup(f'{BASE_URL}/moviereviews')
    if soup:
        links = []
        # Find all review links in the post-thumbnail
        post_thumbnails = soup.find_all('div', class_='post-thumbnail')
        for thumbnail in post_thumbnails:
            link_tag = thumbnail.find('a', href=True)
            if link_tag:
                link = link_tag['href']
                links.append(link)
        return links
    return []

def extract_rating_gulte(soup):
    # Step 1: Find the <strong> tag containing "Rating:"
    rating_tag = soup.find('strong', string=lambda x: x and 'Rating:' in x)
    
    if rating_tag:
        # Step 2: Extract and clean the rating
        rating_text = rating_tag.text.strip().replace("Rating: ", "")
        return rating_text.split("/")[0]  # Extract only the number (e.g., 2.75)
    # Return None if no rating is found
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