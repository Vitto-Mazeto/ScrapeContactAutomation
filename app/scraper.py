from base64 import b64decode
import requests
from bs4 import BeautifulSoup
import re

def fetch_contacts(url, zyte_token):
    print(f"Extraindo contatos de: {url}")
    
    try:
        api_response = requests.post(
            "https://api.zyte.com/v1/extract",
            auth=(zyte_token, ""),
            json={"url": url, "httpResponseBody": True},
        )
        api_response.raise_for_status()
        
        http_response_body = b64decode(api_response.json()["httpResponseBody"])
        html_content = http_response_body.decode("utf-8", errors="ignore")

        soup = BeautifulSoup(html_content, 'html.parser')
        text_elements = soup.find_all(string=True)
        text = ' '.join(text_elements)

        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        cellphone_pattern = r'\(?\b[1-9]{2}\)?[-.\s]?[9]{0,1}\s?[0-9]{4}[-.\s]?[0-9]{4}\b'

        emails = set(re.findall(email_pattern, text))
        cellphones = set(re.findall(cellphone_pattern, text))

        print(f"Contatos extraídos de {url}: Emails: {emails}, Celulares: {cellphones}")

        return {
            'site': url,
            'celular': list(cellphones),
            'email': list(emails),
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
