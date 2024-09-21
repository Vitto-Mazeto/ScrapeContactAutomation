import streamlit as st
import os

from utils import fetch_api_data
from utils import save_api_data

# Caminho do banco de dados
db_path = os.path.join('data', 'contacts.sqlite')

# Função principal da página
def run():
    st.header("Configuração da API Z-API")

    # Exibe o tutorial explicativo
    st.subheader("Tutorial para Configuração da API do WhatsApp")
    st.write("""
    Siga os passos abaixo para configurar sua conexão com a API da Z-API:
    1. Acesse o site da [Z-API](https://z-api.io/) e crie uma conta.
    2. Após criar a conta, crie uma instância ou use a instância padrão.
    3. Após pagar pela sua instância, com o número de telefone que deseja usar, escaneie o QR Code de Conexão com o WhatsApp.
    4. **Lembrando**: Como serão enviadas muitas mensagens iguais, caso queira, por essa aplicação, é recomendado que use um número de telefone novo, pois o WhatsApp pode bloquear o número caso considere como spam.
    5. Acesse o seu dashboard da Z-API e obtenha o **ID da Instância**, **Token** e **URL da API da instância**.
    6. Insira os dados nos campos abaixo e clique em **Salvar**.
    """)

    # Carrega as informações da API do banco de dados
    instance_id, token, api_url = fetch_api_data(db_path)

    # Campos de entrada para os dados da API
    instance_id_input = st.text_input("ID da Instância", value=instance_id)
    token_input = st.text_input("Token da Instância", value=token, type="password")
    api_url_input = st.text_input("URL da API", value=api_url)

    if st.button("Salvar Configurações"):
        save_api_data(db_path, instance_id_input, token_input, api_url_input)
        st.success("Configurações salvas com sucesso!")

if __name__ == "__main__":
    run()
