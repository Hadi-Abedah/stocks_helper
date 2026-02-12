import requests
from bs4 import BeautifulSoup
from pathlib import Path

script_dir = Path(__file__).resolve().parent

def fetch_write_news(search_term, url, news_file):
    """Fetch news for the current search term from the provided URL."""
    
    target_url = f"{url}?q={search_term}"
    resp = requests.get(target_url)
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Extracting the news titles and links
    articles = set(article for article in soup.find_all("a", class_="JtKRv"))
    
    new_titles = []
    
    # Write titles to the file
    with open(news_file, "w") as fhand:
        for article in articles:
            title = article.text.strip()
            link = "https://news.google.com" + article.get("href").removeprefix(".").strip()
            new_titles.append((title, link))
            fhand.write(f"{title}\n{link}\n\n")

    return new_titles

def check_for_new_news(search_term, url):
    """Check for new news by comparing them to the saved titles."""
    
    global script_dir

    news_file = script_dir / f"news_file_{search_term}.txt"

    # Read the old news titles
    old_titles = []
    if news_file.exists():
        with open(news_file, "r") as fhand:
            old_titles = fhand.read().splitlines()
    
    # Fetch and write new titles
    new_titles = fetch_write_news(search_term, url, news_file)

    # Determine what titles are actually new
    new_news_found = False
    for title, link in new_titles:
        if title not in old_titles:
            new_news_found = True
            print(f"New news article found for {search_term}: {title}\nLink: {link}\n")
    
    if not new_news_found:
        print(f"No new news articles found for {search_term}.")

if __name__ == "__main__":
    search_term = "SYM"  # Replace with your desired search term
    url = "https://news.google.com/search"
    
    check_for_new_news(search_term, url)
