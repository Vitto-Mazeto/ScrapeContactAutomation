import streamlit as st
import sqlite3
import os
import random
from mock import mock_fetch_contacts, mock_google_search
from utils import save_contacts_to_db, update_message_count, fetch_all_contacts


def run():
    st.header("Envio Automático ⚡")
    city = st.text_input("Localização", value="São José dos Campos")
    num_results = st.number_input("Número de Resultados", min_value=1, max_value=1000, value=50)

    if st.button("Enviar Mensagens"):
        query = f"terrenos imobiliaria {city}"
        urls = mock_google_search(query, num_results)
        contacts_list = []

        db_path = os.path.join('data', 'contacts.sqlite')

        for url in urls:
            contacts = mock_fetch_contacts(url)
            contacts_list.append(contacts)

        # Gravar os contatos no banco de dados
        save_contacts_to_db(db_path, contacts_list, city)

        # Enviar mensagens e incrementar contador
        for contacts in contacts_list:
            for celular in contacts['celular']:
                update_message_count(db_path, contacts['site'])
                # Simulando envio de mensagem
                st.write(f"Mensagem enviada para {contacts['site']} com número {celular}.")

