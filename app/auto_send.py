import streamlit as st
import os
import random
from utils import save_contacts_to_db, update_message_count, fetch_all_contacts, fetch_api_data, fetch_messages
from search import google_search
from scraper import fetch_contacts
from zapi import send_whats_message

def run():
    st.header("Envio Automático ⚡")
    city = st.text_input("Localização", value="São José dos Campos")
    num_results = st.number_input("Número de Resultados", min_value=1, max_value=1000, value=50)

    if st.button("Enviar Mensagens"):
        query = f"terrenos imobiliaria {city}"
        db_path = os.path.join('data', 'contacts.sqlite')

        # Variável para contar novos contatos adicionados
        new_contacts_added = 0
        start = 0

        # Continuar até adicionar o número necessário de novos contatos
        while new_contacts_added < num_results:
            urls = google_search(query, num_results, start=start)
            contacts_list = []

            for url in urls:
                contacts = fetch_contacts(url)
                contacts_list.append(contacts)

            # Salvar novos contatos no banco de dados e contar quantos foram adicionados
            new_contacts = save_contacts_to_db(db_path, contacts_list, city)
            new_contacts_added += new_contacts

            # Atualiza o start para pegar a próxima página de resultados do Google
            start += 10  # Paginação baseada em múltiplos de 10 para resultados do Google

        st.success(f"{new_contacts_added} novos contatos salvos para {city}")

        # Enviar mensagens para os novos contatos
        if new_contacts_added > 0:
            # Buscar os dados da API e a mensagem pré-salva
            instance_id, token, _ = fetch_api_data(db_path)
            whatsapp_message, _ = fetch_messages(db_path)

            # Verifica se todos os dados necessários para envio estão presentes
            missing_info = []
            if not instance_id:
                missing_info.append("Instance ID")
            if not token:
                missing_info.append("Token")
            if not whatsapp_message:
                missing_info.append("Mensagem do WhatsApp")

            if missing_info:
                st.error(f"Faltando: {', '.join(missing_info)}. Verifique as configurações.")
                return

            # Enviar mensagens aos novos contatos
            for contacts in contacts_list:
                for celular in contacts['celular']:
                    st.write(f"Enviando mensagem para {contacts['site']} com número {celular}...")

                    # Enviar a mensagem usando a Z-API
                    status_code, response = send_whats_message(instance_id, token, celular, whatsapp_message)

                    if status_code == 200:
                        st.success(f"Mensagem enviada para {celular}")
                        # Atualizar contador de mensagens no banco de dados
                        update_message_count(db_path, contacts['site'])
                    else:
                        st.error(f"Falha ao enviar mensagem para {celular}: {response}")

if __name__ == "__main__":
    run()
