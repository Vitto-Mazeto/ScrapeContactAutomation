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

    # Inicializa uma sessão de estado para o DataFrame
    if 'df' not in st.session_state:
        st.session_state.df = df.copy()
    
    # Dropdown para selecionar cidade
    cities = df['Cidade'].unique().tolist()
    selected_city = st.selectbox("Selecione a cidade", options=["Todas"] + cities)

    # Filtra os contatos com base na cidade selecionada
    if selected_city != "Todas":
        df = df[df['Cidade'] == selected_city]
    
    st.session_state.df = df  # Atualiza o DataFrame na sessão de estado

    # Cria colunas para os botões
    col1, col2, col3 = st.columns(3)

    # Botões de seleção e desseleção
    with col1:
        if st.button("Selecionar Todos"):
            st.session_state.df['Selecionar'] = True
    with col2:
        if st.button("Selecionar sem Mensagens"):
            st.session_state.df['Selecionar'] = st.session_state.df['Mensagens Enviadas'] == 0
    with col3:
        if st.button("Desselecionar Todos"):
            st.session_state.df['Selecionar'] = False

    # Exibe o data_editor
    config = {
        "Selecionar": st.column_config.CheckboxColumn(
            "Selecionar",
            help="Selecione as linhas para enviar mensagem",
            default=False
        )
    }
    
    edited_df = st.data_editor(st.session_state.df, column_config=config, hide_index=True)

    # Atualiza o DataFrame na sessão de estado com as alterações feitas pelo usuário
    st.session_state.df.update(edited_df)

    # Atualiza o DataFrame com base nas seleções feitas pelos botões
    if st.button("Disparar Mensagens"):
        selected_contacts = st.session_state.df[st.session_state.df['Selecionar']].to_dict(orient='records')
        if not selected_contacts:
            st.write("Nenhum contato selecionado.")
        else:
            for contact in selected_contacts:
                st.write(f"Enviando mensagem para {contact['Email']} e {contact['Celular']}")
                update_message_count(db_path, contact['Site'])

if __name__ == "__main__":
    run()
