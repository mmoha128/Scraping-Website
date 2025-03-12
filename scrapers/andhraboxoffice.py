import requests
from bs4 import BeautifulSoup

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
                links.append(link)
        return links
    return []

def extract_rating_andhraboxoffice(soup):
    # Step 1: Find the <span> tag containing "Rating:"
    rating_tag = soup.find('span', style='font-weight: bold;', string=lambda x: x and 'Rating:' in x)
    
    if rating_tag:
        # Step 2: Extract and clean the rating
        rating_text = rating_tag.text.strip().replace("Rating: ", "")
        return rating_text.split("/")[0]  # Extract only the number (e.g., 3.25)
    # Return None if no rating is found
    return None

def scrape_movie_details(url):
    soup = get_soup(url)
    if soup:
        # Extract the movie name from the URL or content
        movie_name = url.split('=')[-1].replace('-', ' ').title()

        # Extract the rating using the extract_rating_andhraboxoffice function
        rating = extract_rating_andhraboxoffice(soup)
        if not rating:
            rating = 'No Rating Found'

        return {
            'movie_name': movie_name,
            'rating': rating,
            'url': url
        }
    return None