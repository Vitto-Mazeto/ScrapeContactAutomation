import requests
from bs4 import BeautifulSoup
import re

def fetch_contacts(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        text_elements = soup.find_all(text=True)
        text = ' '.join(text_elements)
        
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        cellphone_pattern = r'\(?\b[1-9]{2}\)?[-.\s]?[9]{0,1}\s?[0-9]{4}[-.\s]?[0-9]{4}\b'

        emails = re.findall(email_pattern, text)
        cellphones = re.findall(cellphone_pattern, text)

        # Remover duplicatas
        emails = list(set(emails))
        cellphones = list(set(cellphones))

        return {
            'site': url,
            'celular': cellphones,
            'email': emails,
        }
    except requests.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return {
            'site': url,
            'celular': [],
            'email': []
        }

if __name__ == "__main__":
    urls = ['https://cortezeimoveis.com.br/', 'https://ribeiroimoveis.com.br/', 'https://www.maiaimoveissjp.com.br/', 'https://venturiimoveis.com.br/', 'https://www.roccoimoveis.com.br/', 'https://alegriaimobiliaria.com.br/', 'https://www.suelifernandes.com/', 'https://www.freitasgodoi.com.br/imoveis/a-venda/terreno/curitiba']
    contacts_list = []

    for url in urls:
        contacts = fetch_contacts(url)
        contacts_list.append(contacts)
    
    for contacts in contacts_list:
        print(contacts)
