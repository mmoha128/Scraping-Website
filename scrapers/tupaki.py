import requests
from bs4 import BeautifulSoup

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
    soup = get_soup(f'{BASE_URL}/movies-reviews')
    if soup:
        links = []
        entertainment_scroll = soup.find_all('div', class_='entertainment-scroll')
        for scroll in entertainment_scroll:
            link_tag = scroll.find('a', href=True)
            if link_tag:
                link = BASE_URL + link_tag['href']
                links.append(link)
        return links
    return []

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
    p_tags = soup.find_all('p')
    
    if p_tags:
        # Get the last <p> tag (which contains the rating)
        last_p = p_tags[-1]
        
        # Extract text while ignoring the <font> tag
        rating_text = ''.join(last_p.find_all(text=True, recursive=False)).strip()
        
        # Extract the numeric rating
        rating = rating_text.split('రేటింగ్-')[-1].strip() if 'రేటింగ్-' in rating_text else "N/A"
        
        return rating
    
    return "N/A" 


def scrape_movie_details(url):
    soup = get_soup(url)
    if soup:
        movie_name = extract_movie_name(soup)
        rating = extract_rating(soup)
        return {
            'movie_name': movie_name,
            'rating': rating,
            'url': url
        }
    return None
