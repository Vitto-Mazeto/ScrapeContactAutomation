import streamlit as st
import os
import sqlite3
from utils import save_contacts_to_db, get_current_links, fetch_zyte_token
from scraper import fetch_contacts
from search import google_search

def run():
    st.header("Buscar Contatos")
    city = st.text_input("Localização", value="São José dos Campos")
    num_results = st.number_input("Número de Resultados", min_value=1, max_value=1000, value=50)

    if st.button("Buscar"):
        try:
            query = f"terrenos imobiliaria {city}"
            db_path = os.path.join('data', 'contacts.sqlite')

            # Recupera as URLs já salvas no banco de dados
            existing_links = get_current_links(db_path)

            # Variável para controlar as URLs processadas
            urls_processed = 0
            start = 0

            # Lista local de URLs já processadas
            processed_urls = set(existing_links)

            zyte_token = fetch_zyte_token(db_path)
            
            progress_bar = st.progress(0)  # Barra de progresso
            status_message = st.empty()  # Espaço para mensagens de status
            
            # Continuar até processar a quantidade solicitada de URLs
            while urls_processed < num_results:
                # Busca novas URLs no Google
                urls = google_search(query, num_results, zyte_token, start=start)
                if not urls:
                    st.info("Nenhuma URL encontrada no Google. Parando a busca.")
                    break

                # Filtra URLs já processadas ou existentes no banco
                new_urls = [url for url in urls if url not in processed_urls]

                if not new_urls:
                    st.info("Nenhuma nova URL encontrada, buscando mais resultados...")
                    start += num_results
                    continue

                contacts_list = []

                for url in new_urls:
                    status_message.write(f'Extraindo contatos de: {url}')  # Exibe a mensagem de extração
                    contacts = fetch_contacts(url, zyte_token)
                    contacts_list.append(contacts)

                    # Marca a URL como processada
                    processed_urls.add(url)
                    urls_processed += 1

                    # Atualiza a barra de progresso com base nas URLs processadas
                    progress_bar.progress(min(urls_processed / num_results, 1.0))

                    # Para de processar se já tiver atingido o número solicitado de URLs
                    if urls_processed >= num_results:
                        break

                # Salva os contatos extraídos no banco de dados
                save_contacts_to_db(db_path, contacts_list, city)
                st.success(f"Contatos processados e Adicionados")

                # Atualiza o start para pegar a próxima leva de URLs do Google
                start += num_results
        except Exception as e:
            print('Ocorreu um erro:', e)

if __name__ == "__main__":
    run()
