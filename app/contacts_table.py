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

    # Oculta a coluna de ID
    df = df.drop(columns=["ID"])

    # Reordena as colunas para colocar 'Selecionar' à esquerda
    cols = ['Selecionar'] + [col for col in df.columns if col != 'Selecionar']
    df = df[cols]

    # Dropdown para selecionar cidade
    cities = df['Cidade'].unique().tolist()
    selected_city = st.selectbox("Selecione a cidade", options=["Todas"] + cities)

    # Filtra os contatos com base na cidade selecionada
    if selected_city != "Todas":
        df = df[df['Cidade'] == selected_city]

    # Inicializa uma sessão de estado para o DataFrame
    if 'df' not in st.session_state:
        st.session_state.df = df

    # Botão para selecionar todos os contatos
    if st.button("Selecionar Todos"):
        st.session_state.df['Selecionar'] = True

    # Botão para selecionar todos os contatos sem mensagens enviadas
    if st.button("Selecionar Todos Sem Mensagens Enviadas"):
        st.session_state.df['Selecionar'] = st.session_state.df['Mensagens Enviadas'] == 0

    config = {
        "Selecionar": st.column_config.CheckboxColumn(
            "Selecionar",
            help="Selecione as linhas para enviar mensagem",
            default=False
        )
    }

    edited_df = st.data_editor(st.session_state.df, column_config=config, hide_index=True)

    if st.button("Disparar Mensagem"):
        selected_contacts = edited_df[edited_df['Selecionar']].to_dict(orient='records')
        if not selected_contacts:
            st.write("Nenhum contato selecionado.")
        else:
            for contact in selected_contacts:
                st.write(f"Enviando mensagem para {contact['Email']} e {contact['Celular']}")
                update_message_count(db_path, contact['Site'])
