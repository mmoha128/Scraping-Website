import requests
from bs4 import BeautifulSoup
import time


def extract_movie_links():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    base_url = "https://www.telugu360.com/category/movies/telugu-movies-reviews"
    all_movie_links = []
    page = 1

    while True:
        url = f"{base_url}/page/{page}/"
        print(f"Fetching page {page}: {url}")
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("Reached end of pagination or encountered error.")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article')

        page_links = []

        for article in articles:
            title = article.find('h2', class_='entry-title')
            if not title:
                cat_cont = article.find('div', class_='cat_cont')
                if cat_cont:
                    title = cat_cont.find('h2', class_='entry-title')

            if title and title.a:
                link = title.a['href']
                if 'review' in link:  # Ensures it's a review link
                    page_links.append(link)

        if not page_links:
            print("No more review links found on this page.")
            break

        # print(f"Found {len(page_links)} review links on page {page}.")
        all_movie_links.extend(page_links)
        page += 1
        time.sleep(1)

    print(f"\nTotal movie links extracted: {len(all_movie_links)}")
    return all_movie_links

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

    # print(f"Extracted Data - Name: {name}, Rating: {rating}")
    return {'MovieName': name, 'Source': url, 'Rating': rating}

