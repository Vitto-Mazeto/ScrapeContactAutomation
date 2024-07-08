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

def search_contacts_page():
    import search_contacts
    search_contacts.run()

def contacts_table_page():
    import contacts_table
    contacts_table.run()

def auto_send_page():
    import auto_send
    auto_send.run()

pg = st.navigation([
    st.Page(search_contacts_page, title="Buscar Contatos", icon="🔍"),
    st.Page(contacts_table_page, title="Tabela de Busca", icon="📋"),
    st.Page(auto_send_page, title="Envio Automático", icon="⚡")
])
pg.run()
