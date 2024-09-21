import streamlit as st
import os

# from mock import mock_fetch_contacts, mock_google_search
from utils import save_contacts_to_db
from scraper import fetch_contacts
from search import google_search

def run():
    st.header("Buscar Contatos")
    city = st.text_input("Localização", value="São José dos Campos")
    num_results = st.number_input("Número de Resultados", min_value=1, max_value=1000, value=50)

    if st.button("Buscar"):
        query = f"terrenos imobiliaria {city}"
        urls = google_search(query, num_results)
        contacts_list = []

        for url in urls:
            contacts = fetch_contacts(url)
            contacts_list.append(contacts)

        db_path = os.path.join('data', 'contacts.sqlite')
        save_contacts_to_db(db_path, contacts_list, city)
        st.success(f"Contatos salvos para {city}")
