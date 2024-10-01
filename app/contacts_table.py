import streamlit as st
import pandas as pd
import os

from zapi import send_whats_message
from utils import delete_all_contacts, fetch_all_contacts, fetch_api_data, fetch_messages, update_message_count

def send_messages(contacts, db_path):
    instance_id, token, _ = fetch_api_data(db_path)
    whatsapp_message, _ = fetch_messages(db_path)

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

    for contact in contacts:
        phone = contact['Celular']
        email = contact['Email']
        site = contact['Site']
        
        st.write(f"Enviando mensagem para {email} e {phone}")
        
        status_code, response = send_whats_message(instance_id, token, phone, whatsapp_message)
        
        if status_code == 200:
            st.success(f"Mensagem enviada para {phone}")
            update_message_count(db_path, site)
        else:
            st.error(f"Falha ao enviar mensagem para {phone}: {response}")

def run():
    st.header("Contatos")
    db_path = os.path.join('data', 'contacts.sqlite')
    contacts = fetch_all_contacts(db_path)

    if not contacts:
        st.write("Nenhum contato encontrado")
        return

    df = pd.DataFrame(contacts, columns=["ID", "Site", "Celular", "Email", "Cidade", "Mensagens Enviadas"])
    df['Selecionar'] = False
    df = df.drop(columns=["ID"])
    cols = ['Selecionar'] + [col for col in df.columns if col != 'Selecionar']
    df = df[cols]

    if 'df' not in st.session_state:
        st.session_state.df = df.copy()
    
    cities = df['Cidade'].unique().tolist()
    selected_city = st.selectbox("Selecione a cidade", options=["Todas"] + cities)

    if selected_city != "Todas":
        filtered_df = st.session_state.df[st.session_state.df['Cidade'] == selected_city].copy()
    else:
        filtered_df = st.session_state.df.copy()

    config = {
        "Selecionar": st.column_config.CheckboxColumn(
            "Selecionar",
            help="Selecione as linhas para enviar mensagem",
            default=False
        )
    }
    
    edited_df = st.data_editor(filtered_df, column_config=config, hide_index=True)
    
    if selected_city != "Todas":
        st.session_state.df.loc[st.session_state.df['Cidade'] == selected_city] = edited_df
    else:
        st.session_state.df = edited_df

    if st.button("Disparar Mensagens Selecionadas"):
        selected_contacts = st.session_state.df[st.session_state.df['Selecionar'] == True].to_dict(orient='records')
        if not selected_contacts:
            st.write("Nenhum contato selecionado.")
        else:
            send_messages(selected_contacts, db_path)
    
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Enviar para Todos"):
            send_messages(filtered_df.to_dict(orient='records'), db_path)

    with col2:
        if st.button("Enviar para Sem Mensagem"):
            contacts_without_messages = filtered_df[filtered_df['Mensagens Enviadas'] == 0]
            send_messages(contacts_without_messages.to_dict(orient='records'), db_path)

    if st.button("Limpar Contatos"):
        delete_all_contacts(db_path)
        st.success("Todos os contatos foram deletados.")
        st.session_state.df = pd.DataFrame(columns=["Site", "Celular", "Email", "Cidade", "Mensagens Enviadas", "Selecionar"])

if __name__ == "__main__":
    run()