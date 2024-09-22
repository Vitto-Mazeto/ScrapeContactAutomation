import os
import streamlit as st
from utils import create_database

# Caminho do banco de dados
db_path = os.path.join('data', 'contacts.sqlite')

# Cria a pasta data se não existir
if not os.path.exists('data'):
    os.makedirs('data')

# Cria o banco de dados se não existir
create_database(db_path)

st.set_page_config(layout="wide")

def search_contacts_page():
    import search_contacts
    search_contacts.run()

def contacts_table_page():
    import contacts_table
    contacts_table.run()

def auto_send_page():
    import auto_send
    auto_send.run()

def define_message_page():
    import define_message
    define_message.run()

def api_config():
    import api_config
    api_config.run()

def import_contacts_page():
    import import_contacts
    import_contacts.run()


pg = st.navigation([
    st.Page(search_contacts_page, title="Buscar Contatos", icon="🔍"),
    st.Page(contacts_table_page, title="Contatos", icon="📋"),
    st.Page(auto_send_page, title="Envio Automático", icon="⚡"),
    st.Page(define_message_page, title="Definir Mensagens", icon="✉️"),
    st.Page(import_contacts_page, title="Importar Contatos", icon="📥"),
    st.Page(api_config, title="Configuração da API", icon="⚙️")
])
pg.run()
