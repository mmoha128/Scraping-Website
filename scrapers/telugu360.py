import requests
from bs4 import BeautifulSoup

def extract_movie_links(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    movie_links = []
    articles = soup.find_all('article')  # Get all article elements

    for article in articles:
        title = article.find('h2', class_='entry-title')
        if not title:
            cat_cont = article.find('div', class_='cat_cont')
            if cat_cont:
                title = cat_cont.find('h2', class_='entry-title')

        if title and title.a:
            link = title.a['href']
            if 'review' in link:  # Ensure it is a review link
                movie_links.append(link)

    print(f"Extracted {len(movie_links)} movie links: {movie_links}")
    return movie_links

def scrape_movie_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract movie name
    name_tag = soup.find('h1', class_='entry-title')  # Corrected title tag
    if name_tag:
        name = name_tag.text.strip()
        if "Movie Review" in name:
            name = name.replace("Movie Review", "").strip()
    else:
        name = "Unknown Movie"

    # Extract rating
    rating = None
    rating_tag = soup.find(string=lambda x: x and 'Telugu360 Rating' in x)
    if rating_tag:
        rating = rating_tag.split("Telugu360 Rating:")[-1].strip()

    print(f"Extracted Data - Name: {name}, Rating: {rating}")
    return {'MovieName': name, 'Source': url, 'Rating': rating}

