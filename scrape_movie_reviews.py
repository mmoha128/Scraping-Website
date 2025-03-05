import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import time

def extract_rating_123telugu(soup):
    rating_tag = soup.find('span', style='color: #ff0000;')
    if rating_tag:
        return rating_tag.text.strip().replace("123telugu.com Rating : ", "")
    return None

def extract_rating_greatandhra(soup):
    rating_tag = soup.find('div', class_='entry-content')
    print(rating_tag)
    if rating_tag:
        return rating_tag.text.strip().replace("Telugu360 Rating:", "")
    return None

def extract_rating_telugu360(soup):
    rating_tag = soup.find('strong', string=lambda x: x and 'Rating:' in x)
    if rating_tag:
        return rating_tag.text.strip().replace("Rating: ", "")
    return None

def extract_rating_m9(soup):
    rating_tag = soup.find('span', style='font-weight: bold;')
    if rating_tag:
        return rating_tag.text.strip().replace("Rating: ", "").split(" ")[0]
    return None

def extract_rating_gulte(soup):
    rating_tag = soup.find('font', color='#ff0000')
    if rating_tag:
        return rating_tag.find_next_sibling(text=True).strip()
    return None

def extract_rating_tupaki(soup):
    rating_tag = soup.find('span', style='font-size: 22px; font-weight: bolder; color: #f00;')
    if rating_tag:
        return rating_tag.text.strip()
    return None

# Function to scrape a single website
def scrape_website(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract movie name (customize based on website)
        if '123telugu.com' in url:
            name_tag = soup.find('h1', class_='entry-title')
            if name_tag:
                name = name_tag.text.strip().split(":")[0]
            else:
                name = "Unknown Movie"
            print(name_tag)
        elif 'greatandhra.com' in url:
            name_tag = soup.find('h1', class_='entry-title')
            if name_tag:
                name = name_tag.text.strip().split(":")[0]
            else:
                name = "Unknown Movie"
            print(name_tag)
        elif 'telugu360.com' in url:
            name_tag = soup.find('h2')
            if name_tag:
                name = name_tag.text.strip()
            else:
                name = "Unknown Movie"
        elif 'm9.news' in url:
            name_tag = soup.find('span', class_='highlighted-red')
            if name_tag:
                name = name_tag.find_next_sibling(text=True).strip().split("–")[0].strip()
            else:
                name = "Unknown Movie"
        elif 'gulte.com' in url:
            name_tag = soup.find('td', class_='txt_inner_bold_green')
            if name_tag:
                name = name_tag.text.strip().split(":")[1].strip().strip("'")
            else:
                name = "Unknown Movie"
        elif 'tupaki.com' in url:
            name_tag = soup.find('h1')
            if name_tag:
                name = name_tag.text.strip().split(":")[0]
            else:
                name = "Unknown Movie"
        else:
            name = "Unknown Movie"
        
        # Extract rating based on website
        if '123telugu.com' in url:
            rating = extract_rating_123telugu(soup)
        elif 'greatandhra.com' in url:
            rating = extract_rating_greatandhra(soup)
        elif 'telugu360.com' in url:
            rating = extract_rating_telugu360(soup)
        elif 'm9.news' in url:
            rating = extract_rating_m9(soup)
        elif 'gulte.com' in url:
            rating = extract_rating_gulte(soup)
        elif 'tupaki.com' in url:
            rating = extract_rating_tupaki(soup)
        else:
            rating = None
        
        return {'MovieName': name, 'Source': url, 'Rating': rating}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# List of websites to scrape
websites = [
    "https://www.123telugu.com",
    "https://telugu.greatandhra.com/movies/reviews/return-of-the-dragon-movie-review.html",
    "https://www.telugu360.com",
    "https://www.m9.news",
    "https://www.gulte.com",
    "https://www.tupaki.com",
    "https://telugu.greatandhra.com/movies/reviews/daaku-maharaaj-movie-review.html"
]

# Database connection
engine = create_engine('sqlite:///movie_reviews.db')

# Scrape all websites
all_data = []
for website in websites:
    print(f"Scraping {website}...")
    data = scrape_website(website)
    if data:
        all_data.append(data)
    time.sleep(10)  # Respect crawl-delay (adjust based on robots.txt)

# Convert to DataFrame
df = pd.DataFrame(all_data)
print(df)  # Check the scraped data

# Save to SQLite database
df.to_sql('movie_reviews', con=engine, if_exists='append', index=False)
print("Data saved to database!")

