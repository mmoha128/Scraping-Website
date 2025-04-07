import time  # Ensure time module is imported
import pandas as pd
from sqlalchemy import create_engine
from scrapers import telugu360, m9news, telugu123, greatandhra, gulte, andhraboxoffice, tupaki  # Import the new Tupaki scraper

# Database connection
engine = create_engine('sqlite:///movie_reviews.db')

def scrape_telugu360():
    print("Scraping Telugu360...")
    review_links = telugu360.extract_movie_links()
    print(f"Extracted {len(review_links)} movie review links: {review_links}")

    for link in review_links:
        data = telugu360.scrape_movie_details(link)
        if data:
            save_to_database(data)
        else:
            print(f"Failed to scrape data from {link}")
    

def scrape_m9news():
    print("Scraping M9 News...")
    review_links = m9news.extract_movie_review_links()
    print(f"Extracted {len(review_links)} movie review links.")

    for link in review_links:
        data = m9news.scrape_movie_details(link)
        if data:
            save_to_database(data)
        else:
            print(f"Failed to scrape data from {link}")

def scrape_123telugu():
    print("Scraping 123telugu...")
    review_links = telugu123.extract_movie_links()
    print(f"Extracted {len(review_links)} movie review links: {review_links}")

    for link in review_links:
        data = telugu123.scrape_movie_details(link)
        if data:
            save_to_database(data)
        else:
            print(f"Failed to scrape data from {link}")

def scrape_greatandhra():
    print("Scraping GreatAndhra...")
    review_links = greatandhra.extract_movie_review_links()
    print(f"Extracted {len(review_links)} movie review links: {review_links}")

    for link in review_links:
        data = greatandhra.scrape_movie_details(link)
        if data:
            save_to_database(data)
        else:
            print(f"Failed to scrape data from {link}")
        

def scrape_gulte():
    print("Scraping Gulte...")
    review_links = gulte.extract_movie_review_links()
    print(f"Extracted {len(review_links)} movie review links: {review_links}")

    for link in review_links:
        data = gulte.scrape_movie_details(link)
        if data:
            save_to_database(data)
        else:
            print(f"Failed to scrape data from {link}")
            
            

### This website has the issue of inconsistent rating format 
def scrape_andhraboxoffice():
    print("Scraping AndhraBoxOffice...")
    review_links = andhraboxoffice.extract_movie_review_links()
    print(f"Extracted {len(review_links)} movie review links: {review_links}")


    for movieName,link in review_links:
        data = andhraboxoffice.scrape_movie_details(movieName,link)
        if data:
            save_to_database(data)
        else:
            print(f"Failed to scrape data from {link}")

def scrape_tupaki():
    print("Scraping Tupaki...")
    review_links = tupaki.extract_movie_review_links()
    print(f"Extracted {len(review_links)} movie review links: {review_links}")

    for link in review_links:
        data = tupaki.scrape_movie_details(link)
        if data:
            save_to_database(data)
        else:
            print(f"Failed to scrape data from {link}")
        
        
def save_to_database(data):
    try:
        df = pd.DataFrame([data]) 
        df.to_sql('movie_reviews', con=engine, if_exists='append', index=False)
        print(f"Saved: {data.get('MovieName', 'Unknown Title')}")
    except Exception as e:
        print(f"Failed to insert data into DB: {e}")

def main():
    # Prompt the user to choose which website to scrape
    print("Which website do you want to scrape?")
    print("1. Telugu360")
    print("2. M9 News")
    print("3. 123telugu")
    print("4. GreatAndhra")
    print("5. Gulte")
    print("6. AndhraBoxOffice")
    print("7. Tupaki")
    choice = input("Enter your choice (1, 2, 3, 4, 5, 6, or 7): ")

    if choice == '1':
        scrape_telugu360()
    elif choice == '2':
        scrape_m9news()
    elif choice == '3':
        scrape_123telugu()
    elif choice == '4':
        scrape_greatandhra()
    elif choice == '5':
        scrape_gulte()
    elif choice == '6':
        scrape_andhraboxoffice()
    elif choice == '7':
        scrape_tupaki()
    else:
        print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6, or 7.")

if __name__ == "__main__":
    main()