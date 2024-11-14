import streamlit as st
import os
import sqlite3
from utils import load_ignored_sites, save_contacts_to_db, get_current_links, fetch_zyte_token, save_ignored_sites
from scraper import fetch_contacts
from search import google_search

def run():
    st.header("Buscar Contatos")
    city = st.text_input("Localização", value="São José dos Campos")
    num_results = st.number_input("Número de Resultados", min_value=1, max_value=1000, value=50)

    db_path = os.path.join('data', 'contacts.sqlite')

    # Carrega sites ignorados
    ignored_sites_text = load_ignored_sites(db_path)
    ignored_sites_input = st.text_area("Sites Ignorados (separados por vírgula)", value=ignored_sites_text)

    if st.button("Buscar"):
        try:
            query = f"terrenos imobiliaria {city}"

            # Salva os sites ignorados
            save_ignored_sites(db_path, ignored_sites_input)

            # Processa lista de sites ignorados para filtragem
            ignored_sites = []
            if ignored_sites_input:
                ignored_sites = [site.strip() for site in ignored_sites_input.split(",") if site.strip()]

            # Resto do código permanece igual
            existing_links = get_current_links(db_path)
            urls_processed = 0
            start = 0
            processed_urls = set(existing_links)

            zyte_token = fetch_zyte_token(db_path)
            if not zyte_token:
                st.warning("Token da Zyte API não configurado. Configure o token na página Configuração da API antes de continuar.")
                return
            
            progress_bar = st.progress(0)
            status_message = st.empty()
            
            while urls_processed < num_results:
                urls = google_search(query, num_results, zyte_token, start=start)
                if not urls:
                    st.info("Nenhuma URL encontrada no Google. Parando a busca.")
                    break

                new_urls = [url for url in urls if url not in processed_urls]

                # Filtra URLs ignoradas apenas se houver sites para ignorar
                if ignored_sites:
                    for ignored_site in ignored_sites:
                        new_urls = [url for url in new_urls if ignored_site not in url]

                if not new_urls:
                    st.info("Nenhuma nova URL encontrada, buscando mais resultados...")
                    start += num_results
                    continue

                contacts_list = []

                for url in new_urls:
                    status_message.write(f'Extraindo contatos de: {url}')
                    contacts = fetch_contacts(url, zyte_token)
                    contacts_list.append(contacts)

                    processed_urls.add(url)
                    urls_processed += 1
                    progress_bar.progress(min(urls_processed / num_results, 1.0))

                    if urls_processed >= num_results:
                        break

                save_contacts_to_db(db_path, contacts_list, city)
                st.success("Contatos processados e adicionados.")

                start += num_results
        except Exception as e:
            st.error(f'Ocorreu um erro: {e}')
            print('Ocorreu um erro:', e)

if __name__ == "__main__":
    run()