import streamlit as st
import sqlite3
import os

from utils import save_messages, fetch_messages

# Caminho do banco de dados
db_path = os.path.join('data', 'contacts.sqlite')

def run():
    st.header("Definir Mensagens")
    
    # Fetch existing messages
    existing_messages = fetch_messages(db_path)
    
    # Create 7 text areas for messages
    messages_dict = {}
    for i in range(7):
        message_value = existing_messages[i] if i < len(existing_messages) else ""
        messages_dict[f"message_{i+1}"] = st.text_area(
            f"Mensagem de WhatsApp {i+1} 💬",
            value=message_value,
            key=f"whatsapp_message_{i+1}"
        )
    
    if st.button("Salvar Mensagens"):
        save_messages(db_path, messages_dict)
        st.success("Mensagens salvas com sucesso!")

if __name__ == "__main__":
    run()
