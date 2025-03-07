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
    # Step 1: Find the <span> tag with style="color: #ff0000;"
    rating_tag = soup.find('span', style='color: #ff0000;')
    
    if rating_tag:
        # Step 2: Extract and clean the rating
        rating_text = rating_tag.text.strip()
        return rating_text.split("/")[0]  # Extract only the number (e.g., 2.5)
    
    # Return None if no rating is found
    return None

def extract_rating_telugu360(soup):
    # Step 1: Find the <strong> tag containing "Telugu360 Rating:"
    rating_tag = soup.find('strong', string=lambda x: x and 'Telugu360 Rating:' in x)
    
    if rating_tag:
        # Step 2: Extract and clean the rating
        rating = rating_tag.text.strip().replace("Telugu360 Rating:", "").strip()
        return rating
    
    # Return None if no rating is found
    return None

def extract_rating_m9(soup):
    # Step 1: Find the <span> tag with the specified style
    rating_tag = soup.find('span', style='font-size: 22px; font-weight: bolder; color: #f00;')
    
    if rating_tag:
        # Step 2: Extract and clean the rating
        rating_text = rating_tag.text.strip()
        return rating_text.split("/")[0]  # Extract only the number (e.g., 2.75)
    
    # Return None if no rating is found
    return None

def extract_rating_gulte(soup):
    # Step 1: Find the <strong> tag containing "Rating:"
    rating_tag = soup.find('strong', string=lambda x: x and 'Rating:' in x)
    
    if rating_tag:
        # Step 2: Extract and clean the rating
        rating_text = rating_tag.text.strip().replace("Rating: ", "")
        return rating_text.split("/")[0]  # Extract only the number (e.g., 2.75)
    
    # Return None if no rating is found
    return None

def extract_rating_tupaki(soup):
    # Step 1: Find the <font> tag with color="#ff0000"
    rating_tag = soup.find('font', color='#ff0000')
    
    if rating_tag:
        # Step 2: Extract the sibling text after the <font> tag
        rating_text = rating_tag.find_next_sibling(string=True).strip().strip('"')
        return rating_text.split("/")[0]  # Extract only the number (e.g., 2)
    
    # Return None if no rating is found
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
                # Extract the text inside the <h1> tag
                full_text = name_tag.text.strip()
                
                # Split the text to isolate the movie name
                # Example: "Review: Aadhi Pinisetty's Sabdham - Caters to niche audiences"
                if "Review:" in full_text:
                    name = full_text.split("Review:")[1].split("-")[0].strip()
                else:
                    name = full_text  # Fallback if "Review:" is not found
            else:
                name = "Unknown Movie"
            
            print(name)  # Debugging: Print the extracted movie name

        elif 'greatandhra.com' in url:
            name_tag = soup.find('h1', class_='entry-title')
            if name_tag:
                name = name_tag.text.strip().split(":")[0]
            else:
                name = "Unknown Movie"
            print(name_tag)
        
        elif 'telugu360.com' in url:
            name_tag = soup.find('h1', class_='post-title')
            if name_tag:
                # Extract the text inside the <h1> tag
                full_text = name_tag.text.strip()
                
                # Split the text to isolate the movie name
                # Example: "Game Changer Movie Review: A Superficial Political Drama!"
                if "Movie Review:" in full_text:
                    name = full_text.split("Movie Review:")[0].strip()
                else:
                    name = full_text  # Fallback if "Movie Review:" is not found
            else:
                name = "Unknown Movie"
            
            print(name)  # Debugging: Print the extracted movie name
        
        elif 'm9.news' in url:
            name_tag = soup.find('div', class_='single-page-title').find('h1')
            if name_tag:
                # Extract the text inside the <h1> tag
                full_text = name_tag.text.strip()
                
                # Split the text to isolate the movie name
                # Example: "Dragon Review: Packs Emotions, If Not Fire"
                if "Review:" in full_text:
                    name = full_text.split("Review:")[0].strip()
                else:
                    name = full_text  # Fallback if "Review:" is not found
            else:
                name = "Unknown Movie"
            
            print(name)  # Debugging: Print the extracted movie name
        
        elif 'gulte.com' in url:
            name_tag = soup.find('h1', class_='name post-title entry-title')
            if name_tag:
                # Extract the text inside the <span> tag within the <h1> tag
                span_tag = name_tag.find('span')
                if span_tag:
                    full_text = span_tag.text.strip()
                    
                    # Split the text to isolate the movie name
                    # Example: "Thandel Movie Review"
                    if "Movie Review" in full_text:
                        name = full_text.split("Movie Review")[0].strip()
                    else:
                        name = full_text  # Fallback if "Movie Review" is not found
                else:
                    name = "Unknown Movie"
            else:
                name = "Unknown Movie"
            
            print(name)  # Debugging: Print the extracted movie name

        elif 'tupaki.com' in url:
            name_tag = soup.find('h1')
            if name_tag:
                # Extract the text inside the <h1> tag
                full_text = name_tag.text.strip()
                
                # Split the text to isolate the movie name
                # Example: "Dragon Review: Packs Emotions, If Not Fire"
                if "Review:" in full_text:
                    name = full_text.split("Review:")[0].strip()
                else:
                    name = full_text  # Fallback if "Review:" is not found
            else:
                name = "Unknown Movie"
            print(name)  # Debugging: Print the extracted movie name
       
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
    "https://www.123telugu.com/reviews/aadhi-pinisetty-sabdham-telugu-movie-review.html",
    "https://telugu.greatandhra.com/movies/reviews/return-of-the-dragon-movie-review.html",
    "https://www.telugu360.com/game-changer-movie-review/",
    "https://www.m9.news/reviews/dragon-tamil-movie-review/",
    "https://www.gulte.com/moviereviews/338661/thandel-movie-review",
    "https://www.tupaki.com/movies-reviews/content-4529",
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

