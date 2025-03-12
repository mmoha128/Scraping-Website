import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.m9.news'

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
    soup = get_soup(f'{BASE_URL}/reviews/')
    if soup:
        links = []
        # Find all archive items
        archive_items = soup.find_all('div', class_='archive-item')
        for item in archive_items:
            # Find the <a> tag inside the archive item
            link_tag = item.find('a', href=True)
            if link_tag:
                link = link_tag['href']
                # Ensure the link is absolute
                if link.startswith('/'):
                    link = BASE_URL + link
                links.append(link)
        return links
    return []

def scrape_movie_details(url):
    soup = get_soup(url)
    if soup:
        # Extract the movie name from the URL
        movie_name = url.split('/')[-2].replace('-', ' ').title()

        # Step 1: Find the <span> tag with the specified style
        rating_tag = soup.find('span', style='font-size: 22px; font-weight: bolder; color: #f00;')
        
        if rating_tag:
            # Step 2: Extract and clean the rating
            rating_text = rating_tag.text.strip()
            rating = rating_text.split("/")[0]  # Extract only the number (e.g., 2.75)
        else:
            rating = 'No Rating Found'

        return {
            'movie_name': movie_name,
            'rating': rating,
            'url': url
        }
    return None