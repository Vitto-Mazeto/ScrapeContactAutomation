import sqlite3
import os
import random
import streamlit as st
import pandas as pd

# Função mockada para google_search
def mock_google_search(query, num_results):
    return [f"https://example.com/{i}" for i in range(num_results)]

# Função mockada para fetch_contacts
def mock_fetch_contacts(url):
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

def fetch_all_contacts(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    conn.close()
    return rows

def main():
    # Cria a pasta data se não existir
    if not os.path.exists('data'):
        os.makedirs('data')

    db_path = os.path.join('data', 'contacts.sqlite')

    # Cria o banco de dados se não existir
    create_database(db_path)

    st.title("RPA Contatos de Imobiliárias")

    tab1, tab2 = st.tabs(["Buscar Contatos", "Tabela de busca"])

    with tab1:
        st.header("Buscar Contatos")
        city = st.text_input("Localização", value="São José dos Campos")
        num_results = st.number_input("Número de Resultados", min_value=1, max_value=1000, value=50)

        if st.button("Buscar"):
            query = f"terrenos imobiliaria {city}"
            urls = mock_google_search(query, num_results)
            contacts_list = []

            for url in urls:
                contacts = mock_fetch_contacts(url)
                contacts_list.append(contacts)

            save_contacts_to_db(db_path, contacts_list, city)
            st.success(f"Contatos salvos para {city}")

    with tab2:
        st.header("Contatos")
        contacts = fetch_all_contacts(db_path)

        if contacts:
            df = pd.DataFrame(contacts, columns=["ID", "Site", "Celular", "Email", "Cidade"])
            st.dataframe(df)
        else:
            st.write("Sem contatos até o momento.")

if __name__ == "__main__":
    main()
