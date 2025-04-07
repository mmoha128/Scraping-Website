import requests
from bs4 import BeautifulSoup
import re

BASE_URL = 'http://andhraboxoffice.com'

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
    soup = get_soup(f'{BASE_URL}/More.aspx?cid=12')
    if soup:
        links = []
        # Find all review links in the table rows
        tables = soup.find_all('table', width="100%", border="0", cellspacing="2", cellpadding="1")
        for table in tables:
            link_tag = table.find('a', href=True, class_='side_link')
            if link_tag:
                link = BASE_URL + '/' + link_tag['href']
                movie_name = link_tag.text.strip()
                # Skip "ShareOnFB" entries
                if movie_name.lower() != "shareonfb":
                    links.append((movie_name, link))
        return links
    return []

def extract_rating_andhraboxoffice(soup):
    # Step 1: Find the <span> tag containing "Overall Movie Rating"
    rating_tag = soup.find(
        lambda tag: tag.name in ["div", "p"] and re.search(
            r"^(Movie rating:|Rating:|Overall Movie Rating)", 
            tag.get_text(strip=True), 
            re.IGNORECASE
        )
    )
    if rating_tag:
        # Step 2: Extract the text and clean it
        rating_text = rating_tag.text.strip()
        match = re.search(r'\d+(\.\d+)?', rating_text)
        if match:
            rating_value = match.group()
            return rating_value
        else:
            print("No rating number found.")
    return None

def scrape_movie_details(movie_name,url):
    soup = get_soup(url)
    if soup:
        # Extract the rating using the extract_rating_andhraboxoffice function
        rating = extract_rating_andhraboxoffice(soup)
        if not rating:
            rating = 'No Rating Found'

        return {
            'MovieName': movie_name,
            'Source': url,
            'Rating': rating
        }
    return None
