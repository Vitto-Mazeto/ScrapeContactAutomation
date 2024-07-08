import streamlit as st
import pandas as pd
import sqlite3
import os

from utils import fetch_all_contacts, update_message_count

def run():
    st.header("Contatos")
    db_path = os.path.join('data', 'contacts.sqlite')
    contacts = fetch_all_contacts(db_path)

    # Se não houver contatos, exibe mensagem e retorna
    if not contacts:
        st.write("Nenhum contato encontrado")
        return

    df = pd.DataFrame(contacts, columns=["ID", "Site", "Celular", "Email", "Cidade", "Mensagens Enviadas"])
    df['Selecionar'] = False

    # Dropdown para selecionar cidade
    cities = df['Cidade'].unique().tolist()
    selected_city = st.selectbox("Selecione a cidade", options=["Todas"] + cities)

    # Filtra os contatos com base na cidade selecionada
    if selected_city != "Todas":
        df = df[df['Cidade'] == selected_city]

    # Botão para selecionar todos os contatos
    if st.button("Selecionar Todos"):
        df['Selecionar'] = True

    # Botão para selecionar todos os contatos sem mensagens enviadas
    if st.button("Selecionar Todos Sem Mensagens Enviadas"):
        df.loc[df['Mensagens Enviadas'] == 0, 'Selecionar'] = True

    config = {
        "Selecionar": st.column_config.CheckboxColumn(
            "Selecionar",
            help="Selecione as linhas para enviar mensagem",
            default=False
        )
    }

    edited_df = st.data_editor(df, column_config=config, hide_index=True)

    if st.button("Disparar Mensagem"):
        selected_contacts = edited_df[edited_df['Selecionar']].to_dict(orient='records')
        for contact in selected_contacts:
            st.write(f"Enviando mensagem para {contact['Email']} e {contact['Celular']}")
            update_message_count(db_path, contact['Site'])
            df.loc[df['Email'] == contact['Email'], 'Mensagens Enviadas'] += 1
