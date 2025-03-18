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
                movie_name = link_tag.text.strip()
                # Skip "ShareOnFB" entries
                if movie_name.lower() != "shareonfb":
                    links.append((movie_name, link))
                    # Debug: Print the extracted link and movie name
                    print(f"Extracted link: {link}")
                    print(f"Movie name: {movie_name}")
        return links
    return []

def extract_rating_andhraboxoffice(soup):
    # Step 1: Find the <span> tag containing "Overall Movie Rating"
    rating_tag = soup.find('span', style='font-family: Trebuchet MS;')
    if rating_tag:
        # Step 2: Extract the text and clean it
        rating_text = rating_tag.text.strip()
        if "Overall Movie Rating" in rating_text:
            # Extract the rating value (e.g., "2.75 / 5")
            rating_value = rating_text.split("Overall Movie Rating")[1].split(":")[1].strip().split("/")[0].strip()
            # Debug: Print the extracted rating
            print(f"Extracted rating: {rating_value}")
            return rating_value
    # Debug: Print if no rating is found
    print("No rating found.")
    return None

def scrape_movie_details(url):
    soup = get_soup(url)
    if soup:
        # Extract the movie name
        movie_name_tag = soup.find('a', class_='side_link')
        if movie_name_tag:
            movie_name = movie_name_tag.text.strip()
        else:
            movie_name = "Unknown Movie"

        # Extract the rating using the extract_rating_andhraboxoffice function
        rating = extract_rating_andhraboxoffice(soup)
        if not rating:
            rating = 'No Rating Found'

        # Debug: Print the final extracted data
        print(f"Final data: Movie Name = {movie_name}, Rating = {rating}, URL = {url}")

        return {
            'movie_name': movie_name,
            'rating': rating,
            'url': url
        }
    return None
