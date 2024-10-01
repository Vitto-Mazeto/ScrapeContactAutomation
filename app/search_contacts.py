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
        db_path = os.path.join('data', 'contacts.sqlite')
        
        # Variável para controlar os novos contatos adicionados
        new_contacts_added = 0
        start = 0
        
        # Continuar até adicionar o número necessário de novos contatos
        while new_contacts_added < num_results:
            urls = google_search(query, num_results, start=start)
            contacts_list = []

            for url in urls:
                print('Fetching contacts from:', url)
                contacts = fetch_contacts(url)
                contacts_list.append(contacts)

            # Tenta adicionar os contatos ao banco de dados, e conta quantos são novos
            new_contacts = save_contacts_to_db(db_path, contacts_list, city)
            new_contacts_added += new_contacts

            # Atualiza o start para pegar a próxima página de resultados do Google
            start += 10  # Ou outro valor baseado na paginação de resultados

        st.success(f"{new_contacts_added} novos contatos salvos para {city}")
