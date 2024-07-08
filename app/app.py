import sqlite3
import os
import random

# Função mockada para google_search
def mock_google_search(query, num_results):
    # Retorna uma lista de URLs mockadas
    return [f"https://example.com/{i}" for i in range(num_results)]

# Função mockada para fetch_contacts
def mock_fetch_contacts(url):
    # Retorna um dicionário com contatos mockados
    return {
        'site': url,
        'celular': [f"({random.randint(10, 99)}) {random.randint(90000, 99999)}-{random.randint(1000, 9999)}"],
        'email': [f"email{random.randint(1, 100)}@example.com"]
    }

def create_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site TEXT,
        celular TEXT,
        email TEXT,
        city TEXT
    )
    ''')
    conn.commit()
    conn.close()

def save_contacts_to_db(db_path, contacts_list, city):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for contacts in contacts_list:
        for celular in contacts['celular']:
            for email in contacts['email']:
                cursor.execute('''
                INSERT INTO contacts (site, celular, email, city) VALUES (?, ?, ?, ?)
                ''', (contacts['site'], celular, email, city))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    city = "Santiago"
    query = f"terrenos imobiliaria {city}"
    num_results = 50

    # Criar a pasta data se não existir
    if not os.path.exists('data'):
        os.makedirs('data')

    db_path = os.path.join('data', 'contacts.sqlite')

    # Criar o banco de dados se não existir
    create_database(db_path)

    urls = mock_google_search(query, num_results)
    contacts_list = []

    for url in urls:
        contacts = mock_fetch_contacts(url)
        contacts_list.append(contacts)

    # Salvar a contacts_list no banco de dados
    save_contacts_to_db(db_path, contacts_list, city)

    print("Contacts saved to", db_path)
