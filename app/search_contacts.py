import streamlit as st
import sqlite3
import os
import random

from utils import create_database, save_contacts_to_db

def mock_google_search(query, num_results):
    return [f"https://example.com/{i}" for i in range(num_results)]

def mock_fetch_contacts(url):
    return {
        'site': url,
        'celular': [f"({random.randint(10, 99)}) {random.randint(90000, 99999)}-{random.randint(1000, 9999)}"],
        'email': [f"email{random.randint(1, 100)}@example.com"]
    }

def run():
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

        db_path = os.path.join('data', 'contacts.sqlite')
        save_contacts_to_db(db_path, contacts_list, city)
        st.success(f"Contatos salvos para {city}")
