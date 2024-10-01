import streamlit as st
import os
import sqlite3
from utils import save_contacts_to_db, get_current_links
from scraper import fetch_contacts
from search import google_search

def run():
    st.header("Buscar Contatos")
    city = st.text_input("Localização", value="São José dos Campos")
    num_results = st.number_input("Número de Resultados", min_value=1, max_value=1000, value=50)

    if st.button("Buscar"):
        query = f"terrenos imobiliaria {city}"
        db_path = os.path.join('data', 'contacts.sqlite')
        
        # Recupera as URLs já salvas no banco de dados
        existing_links = get_current_links(db_path)
        
        # Variável para controlar os novos contatos adicionados
        new_contacts_added = 0
        start = 0
        
        # Mantém uma lista local de URLs já processadas durante a execução
        processed_urls = set(existing_links)
        
        # Continuar até adicionar o número necessário de novos contatos
        while new_contacts_added < num_results:
            # Busca novas URLs no Google
            urls = google_search(query, num_results, start=start)
            
            # Filtra URLs que já estão no banco de dados ou já foram processadas nesta execução
            new_urls = [url for url in urls if url not in processed_urls]
            
            if not new_urls:
                st.info("Nenhuma nova URL encontrada, buscando mais resultados...")
                # Atualiza o start para pegar a próxima leva de resultados do Google
                start += num_results
                continue  # Continua buscando mais resultados

            contacts_list = []

            for url in new_urls:
                print('Fetching contacts from:', url)
                contacts = fetch_contacts(url)
                contacts_list.append(contacts)
                
                # Marca a URL como processada
                processed_urls.add(url)

            # Tenta adicionar os contatos ao banco de dados, e conta quantos são novos
            new_contacts = save_contacts_to_db(db_path, contacts_list, city)
            new_contacts_added += new_contacts

            # Atualiza o start para pegar a próxima leva de resultados do Google
            start += num_results

        st.success(f"{new_contacts_added} novos contatos salvos para {city}")
