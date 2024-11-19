import streamlit as st
import pandas as pd
import os
import random
import time

from zapi import send_whats_message, send_whatsapp_message_evolution
from utils import delete_all_contacts, fetch_all_contacts, fetch_api_data, fetch_messages, update_message_count

def send_messages(contacts, db_path, max_messages, min_interval, max_interval, interval_after, long_min_interval, long_max_interval):
    whatsapp_messages = fetch_messages(db_path)
    
    if not whatsapp_messages:
        st.error("Nenhuma mensagem de WhatsApp cadastrada. Verifique as configurações.")
        return
    
    for i, contact in enumerate(contacts):
        if i >= max_messages:
            st.warning("Limite de mensagens atingido.")
            break
        
        phone = contact['Celular']
        st.write(f"Enviando mensagem para {phone}")
        
        # Randomly select a message from available messages
        selected_message = random.choice(whatsapp_messages)

        print(f"Sending message to {phone}: {selected_message}")
        
        # Send the message
        # status_code, response = send_whats_message(instance_id, token, phone, selected_message, client_token)
        response = send_whatsapp_message_evolution(phone, selected_message)
        
        if response:
            st.success(f"Mensagem enviada para {phone}")
            update_message_count(db_path, phone)
        else:
            st.error(f"Falha ao enviar mensagem para {phone}")
        
        # Handle intervals
        if (i + 1) % interval_after == 0:
            wait_time = random.uniform(long_min_interval, long_max_interval)
            st.write(f"Pausando por {wait_time:.2f} segundos após {interval_after} mensagens.")
        else:
            wait_time = random.uniform(min_interval, max_interval)
            st.write(f"Intervalo entre mensagens: {wait_time:.2f} segundos.")
        
        time.sleep(wait_time)

def run():
    st.header("Contatos")
    db_path = os.path.join('data', 'contacts.sqlite')
    contacts = fetch_all_contacts(db_path)

    if not contacts:
        st.write("Nenhum contato encontrado")
        return

    # Seção de rating das mensagens
    st.subheader("Configuração de Envio de Mensagens")

    # Dividindo em duas colunas
    col4, col5 = st.columns(2)

    with col4:
        # Campo para limitar até X mensagens
        max_messages = st.number_input("Limite de mensagens", min_value=1, max_value=1000, value=50)
        
        # Campo para definir o intervalo entre cada mensagem
        min_interval = st.slider("Intervalo mínimo entre mensagens (segundos)", min_value=1, max_value=60, value=5)

        # Campo para definir o intervalo máximo entre cada mensagem
        max_interval = st.slider("Intervalo máximo entre mensagens (segundos)", min_value=1, max_value=120, value=15)


    with col5:
        # Campo para definir um intervalo maior após Y mensagens
        interval_after = st.number_input("Pausar após quantas mensagens?", min_value=1, max_value=100, value=10)

        # Campo para definir um intervalo longo mínimo após Y mensagens
        long_min_interval = st.slider("Intervalo longo mínimo (segundos)", min_value=10, max_value=600, value=30)

        # Campo para definir um intervalo longo máximo após Y mensagens
        long_max_interval = st.slider("Intervalo longo máximo (segundos)", min_value=10, max_value=1200, value=60)

    # Configuração de cidade e contatos
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
                send_messages(
                    selected_contacts.to_dict(orient='records'), db_path, max_messages, min_interval, 
                    max_interval, interval_after, long_min_interval, long_max_interval
                )
            else:
                st.warning("Nenhum contato selecionado")

    with col2:
        if st.button("Enviar para Todos"):
            send_messages(
                filtered_df.drop(columns=['Selecionar']).to_dict(orient='records'), db_path, max_messages, 
                min_interval, max_interval, interval_after, long_min_interval, long_max_interval
            )

    with col3:
        if st.button("Enviar para Sem Mensagem"):
            contacts_without_messages = filtered_df[filtered_df['Mensagens Enviadas'] == 0]
            send_messages(
                contacts_without_messages.drop(columns=['Selecionar']).to_dict(orient='records'), db_path, max_messages, 
                min_interval, max_interval, interval_after, long_min_interval, long_max_interval
            )

    if st.button("Limpar Contatos"):
        delete_all_contacts(db_path)
        st.success("Todos os contatos foram deletados.")

if __name__ == "__main__":
    run()
