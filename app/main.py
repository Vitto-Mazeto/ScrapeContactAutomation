import streamlit as st

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
