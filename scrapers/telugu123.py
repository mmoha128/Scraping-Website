import requests
from bs4 import BeautifulSoup
import time


def extract_movie_links():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    BASE_URL = 'https://www.123telugu.com'
    page = 1
    all_links = []

    while True:
        url = f"{BASE_URL}/category/reviews/page/{page}"
        print(f"Fetching: {url}")
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Page {page} not reachable. Stopping.")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        movie_links = []
        
        for item in soup.find_all('div', class_='pcsl-item'):
            title_div = item.find('div', class_='pcsl-title')
            if title_div and title_div.a:
                link = title_div.a['href']
                title_text = title_div.a.text.strip().lower()

                # Filter: Must be a review and not OTT or web series
                if '/reviews/' in link and 'ott review' not in title_text and 'web series' not in title_text:
                    movie_links.append(link)

        if not movie_links:
            print("No valid movie links found on this page. Ending.")
            break

        print(f"Page {page}: Found {len(movie_links)} links.")
        all_links.extend(movie_links)
        page += 1
        time.sleep(1)
    return all_links

def scrape_movie_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract movie name
    name_tag = soup.find('h1', class_='entry-title')
    if name_tag:
        name = name_tag.text.strip()
        # Clean the name to remove "Review :" or similar prefixes
        if "Review :" in name:
            name = name.split("Review :")[1].strip()
        elif "Review:" in name:
            name = name.split("Review:")[1].strip()
    else:
        name = "Unknown Movie"
    
    # Extract rating
    rating_tag = soup.find('span', style='color: #ff0000;')
    if rating_tag:
        rating = rating_tag.text.strip().replace("123telugu.com Rating : ", "")
    else:
        rating = None
    
    # Debug: Print the extracted data
    print(f"Extracted data: {name}, {rating}")
    return {'MovieName': name, 'Source': url, 'Rating': rating}