from base64 import b64decode
import requests
from bs4 import BeautifulSoup
import time
import random

from scraper import fetch_contacts

def google_search(query, num_results, zyte_token, start=0):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    search_results = []
    # Adicionando o parâmetro `start` para controlar o offset dos resultados de pesquisa
    url = f"https://www.google.com/search?q={query}&num={num_results}&start={start}"

    api_response = requests.post(
            "https://api.zyte.com/v1/extract",
            auth=(zyte_token, ""),
            json={
                "url": url,
                "httpResponseBody": True,
            },
        )
    api_response.raise_for_status()
    http_response_body = b64decode(api_response.json()["httpResponseBody"])
    html_content = http_response_body.decode("utf-8")
    soup = BeautifulSoup(html_content, 'html.parser')
    
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

