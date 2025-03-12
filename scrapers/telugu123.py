import requests
from bs4 import BeautifulSoup

def extract_movie_links(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all movie review links
    movie_links = []
    for item in soup.find_all('div', class_='pcsl-item'):
        title_div = item.find('div', class_='pcsl-title')
        if title_div and title_div.a:
            link = title_div.a['href']
            title_text = title_div.a.text.strip().lower()
            
            # Filter out OTT reviews and web series
            if '/reviews/' in link and 'ott review' not in title_text and 'web series' not in title_text:
                movie_links.append(link)
    
    # Debug: Print the extracted links
    print(f"Extracted {len(movie_links)} movie links: {movie_links}")
    return movie_links

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