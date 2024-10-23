from base64 import b64decode
import requests
from bs4 import BeautifulSoup
import re

def fetch_contacts(url, zyte_token):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        print(f"Extraindo contatos de: {url}")
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
        try:
            html_content = http_response_body.decode("utf-8")
        except UnicodeDecodeError:
            print(f"Erro ao decodificar o corpo da resposta como UTF-8 para {url}")
            return {
                'site': url,
                'celular': [],
                'email': []
            }
        soup = BeautifulSoup(html_content, 'html.parser')

        text_elements = soup.find_all(string=True)
        text = ' '.join(text_elements)
        
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        cellphone_pattern = r'\(?\b[1-9]{2}\)?[-.\s]?[9]{0,1}\s?[0-9]{4}[-.\s]?[0-9]{4}\b'

        emails = re.findall(email_pattern, text)
        cellphones = re.findall(cellphone_pattern, text)

        # Remover duplicatas
        emails = list(set(emails))
        cellphones = list(set(cellphones))
        print(f"Contatos extraídos de {url}: {emails}, {cellphones}")

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
    url_sem_contato = ['https://www.silverioimobiliaria.com.br/imoveis/a-venda/terreno/sao-jose-dos-campos']
    contacts_list = []

    for url in urls:
        contacts = fetch_contacts(url, '4b72557563ae432f93a4973ec1edcf54')
        contacts_list.append(contacts)
    
    for contacts in contacts_list:
        print(contacts)
