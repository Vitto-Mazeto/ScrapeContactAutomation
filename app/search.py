import requests
from bs4 import BeautifulSoup
import time
import random

from scraper import fetch_contacts

def google_search(query, num_results):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    search_results = []
    url = f"https://www.google.com/search?q={query}&num={num_results}"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for item in soup.find_all('div', attrs={'class': 'g'}):
        # Ignora links patrocinados e "sponsored" -> a melhorar
        if 'sponsored' in item.text.lower() or 'ad' in item.text.lower():
            continue

        link = item.find('a', href=True)
        if link:
            search_results.append(link['href'])
        if len(search_results) >= num_results:
            break
    
    return search_results

