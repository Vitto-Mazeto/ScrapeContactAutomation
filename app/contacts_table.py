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
