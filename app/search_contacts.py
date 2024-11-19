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
            success_message = st.empty()
            
            while urls_processed < num_results:
                urls = google_search(query, num_results, zyte_token, start=start)
                if not urls:
                    st.info("Nenhuma URL encontrada no Google. Parando a busca.")
                    break

                new_urls = [url for url in urls if url not in processed_urls]

                # Filtra URLs ignoradas
                if ignored_sites:
                    for ignored_site in ignored_sites:
                        new_urls = [url for url in new_urls if ignored_site not in url]

                if not new_urls:
                    st.info("Nenhuma nova URL encontrada, buscando mais resultados...")
                    start += num_results
                    continue

                for url in new_urls:
                    try:
                        status_message.write(f'Extraindo contatos de: {url}')
                        contacts = fetch_contacts(url, zyte_token)
                        
                        # Salva o contato imediatamente após a extração
                        if contacts:
                            save_contacts_to_db(db_path, [contacts], city)
                            success_message.success(f"Contato salvo com sucesso: {url}")

                        processed_urls.add(url)
                        urls_processed += 1
                        progress_bar.progress(min(urls_processed / num_results, 1.0))

                    except Exception as e:
                        st.error(f'Erro ao processar URL {url}: {e}')
                        continue

                    if urls_processed >= num_results:
                        break

                start += num_results

            st.success(f"Processo finalizado. Total de URLs processadas: {urls_processed}")
        except Exception as e:
            st.error(f"Erro ao buscar contatos: {e}")

if __name__ == "__main__":
    run()