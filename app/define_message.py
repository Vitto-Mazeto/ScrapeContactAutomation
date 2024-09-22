import streamlit as st
import sqlite3
import os

from utils import save_messages, fetch_messages

# Caminho do banco de dados
db_path = os.path.join('data', 'contacts.sqlite')

def run():
    st.header("Definir Mensagens")

    # Carrega as mensagens existentes do banco de dados
    whatsapp_message, email_message = fetch_messages(db_path)

    # Campos de texto para definir mensagens
    whatsapp_message_input = st.text_area("Mensagem de WhatsApp 💬", value=whatsapp_message)
    # email_message_input = st.text_area("Mensagem de Email ✉️", value=email_message)

    if st.button("Salvar Mensagens"):
        save_messages(db_path, whatsapp_message_input, "")
        st.success("Mensagens salvas com sucesso!")

if __name__ == "__main__":
    run()
