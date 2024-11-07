import streamlit as st
import pandas as pd
import os

from zapi import send_whats_message
from utils import delete_all_contacts, fetch_all_contacts, fetch_api_data, fetch_messages, update_message_count

def send_messages(contacts, db_path):
    instance_id, token, api_url, client_token = fetch_api_data(db_path)
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

    # Itera sobre os contatos selecionados e envia as mensagens
    for contact in contacts:
        phone = contact['Celular']
        st.write(f"Enviando mensagem para {phone}")
        
        status_code, response = send_whats_message(instance_id, token, phone, whatsapp_message, client_token)
        
        if status_code == 200:
            st.success(f"Mensagem enviada para {phone}")
            update_message_count(db_path, phone)
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
    df = df.drop(columns=["ID"])

    # Filtro de cidade
    cities = df['Cidade'].unique().tolist()
    selected_city = st.selectbox("Selecione a cidade", options=["Todas"] + cities)

    if selected_city != "Todas":
        filtered_df = df[df['Cidade'] == selected_city]
    else:
        filtered_df = df.copy()

    # Adiciona uma coluna de checkbox no início
    filtered_df.insert(0, 'Selecionar', False)
    
    # Cria uma cópia do DataFrame para evitar o aviso do Streamlit
    edited_df = st.data_editor(
        filtered_df,
        hide_index=True,
        column_config={
            "Selecionar": st.column_config.CheckboxColumn(
                "Selecionar",
                help="Selecione os contatos para enviar mensagem",
                default=False,
            )
        }
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Enviar para Selecionados"):
            selected_contacts = edited_df[edited_df['Selecionar']].drop(columns=['Selecionar'])
            st.success(f"Enviando mensagem para {len(selected_contacts)} contatos selecionados")
            if len(selected_contacts) > 0:
                send_messages(selected_contacts.to_dict(orient='records'), db_path)
            else:
                st.warning("Nenhum contato selecionado")

    with col2:
        if st.button("Enviar para Todos"):
            send_messages(filtered_df.drop(columns=['Selecionar']).to_dict(orient='records'), db_path)

    with col3:
        if st.button("Enviar para Sem Mensagem"):
            contacts_without_messages = filtered_df[filtered_df['Mensagens Enviadas'] == 0]
            send_messages(contacts_without_messages.drop(columns=['Selecionar']).to_dict(orient='records'), db_path)

    if st.button("Limpar Contatos"):
        delete_all_contacts(db_path)
        st.success("Todos os contatos foram deletados.")

if __name__ == "__main__":
    run()