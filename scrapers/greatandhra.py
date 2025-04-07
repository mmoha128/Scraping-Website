import requests
from bs4 import BeautifulSoup
import time

BASE_URL = 'https://telugu.greatandhra.com'

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
        url = f'{BASE_URL}/movies/reviews/page/{page}/'
        print(f"Fetching: {url}")
        soup = get_soup(url)

        if not soup:
            print(f"Stopping at page {page}. No content.")
            break

        entry_titles = soup.find_all('h2', class_='entry-title')
        if not entry_titles:
            print(f"No reviews found on page {page}. Ending pagination.")
            break

        page_links = []
        for title in entry_titles:
            link_tag = title.find('a', href=True)
            if link_tag:
                link = link_tag['href']
                page_links.append(link)

        print(f"Page {page}: Found {len(page_links)} links.")
        all_links.extend(page_links)
        page += 1
        time.sleep(1)

    return all_links


def extract_rating_greatandhra(soup):
    # Step 1: Find the <span> tag with style="color: #ff0000;"
    rating_tag = soup.find('span', style='color: #ff0000;')
    
    if rating_tag:
        # Step 2: Extract and clean the rating
        rating_text = rating_tag.text.strip()
        return rating_text.split("/")[0]  # Extract only the number (e.g., 2.5)
    # Return None if no rating is found
    return None

def scrape_movie_details(url):
    soup = get_soup(url)
    if soup:
        # Extract the movie name from the URL
        movie_name = url.split('/')[-1].replace('-', ' ').replace('.html', '').title()

        # Extract the rating using the extract_rating_greatandhra function
        rating = extract_rating_greatandhra(soup)
        if not rating:
            rating = 'No Rating Found'

        return {
            'MovieName': movie_name,
            'Source': url,
            'rating': rating
        }
    return None