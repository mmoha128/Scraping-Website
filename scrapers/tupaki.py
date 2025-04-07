import requests
from bs4 import BeautifulSoup
import re

BASE_URL = 'https://www.tupaki.com'

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
    links = []
    page = 1
    
    while True:
        url = f'{BASE_URL}/movies-reviews/{page}' if page > 1 else f'{BASE_URL}/movies-reviews'
        print(f"Scraping page {page}: {url}")
        soup = get_soup(url)
        
        if not soup:
            break

        new_links = []
        entertainment_scroll = soup.find_all('div', class_='entertainment-scroll')
        for scroll in entertainment_scroll:
            link_tag = scroll.find('a', href=True)
            if link_tag:
                link = BASE_URL + link_tag['href']
                new_links.append(link)

        if not new_links:
            print("No more review links found. Ending pagination.")
            break

        links.extend(new_links)
        page += 1

    print(f"\nTotal {len(links)} movie review links extracted.")
    return links


def extract_movie_name(soup):
    """ Extracts movie name from the page, checking multiple possible locations. """
    name_tag = soup.find('div', class_='no-padding')
    if name_tag:
        p_tag = name_tag.find('p')
        if p_tag:
            return p_tag.text.strip()
    
    # Alternative extraction: Try finding the first heading as a fallback
    heading_tag = soup.find('h1') or soup.find('h2') or soup.find('h3')
    if heading_tag:
        return heading_tag.text.strip()

    return "Unknown Movie"


def extract_rating(soup):
    # Find all <p> tags inside the div
    rating_tag = soup.find(
        lambda tag: tag.name in ["div", "p"] and re.search(
            r"^(రేటింగ్-)", 
            tag.get_text(strip=True), 
            re.IGNORECASE
        )
    )
    if rating_tag:
        # Extract the text and clean it
        rating_text = rating_tag.text.strip()
        match = re.search(r'\d+(\.\d+)?', rating_text)
        if match:
            rating_value = match.group()
            return rating_value
        else:
            print("No rating number found.")
    
    return "N/A" 


def scrape_movie_details(url):
    soup = get_soup(url)
    if soup:
        movie_name = extract_movie_name(soup)
        rating = extract_rating(soup)
        return {
            'MovieName': movie_name,
            'Source': url,
            'Rating': rating
        }
    return None
