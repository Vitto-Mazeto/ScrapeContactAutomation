import streamlit as st

def run():
    st.title("Manual da Aplicação: Extrator de Contatos de Terrenos Imobiliários")
    
    st.header("Visão Geral")
    st.markdown("""
    Esta aplicação foi desenvolvida para auxiliar na extração de contatos (celular e e-mail) de diversas imobiliárias que vendem terrenos em uma determinada cidade. Através dela, você pode automatizar o envio de mensagens para essas imobiliárias via WhatsApp, utilizando a integração com o Z-API.

    A seguir, você encontrará uma descrição detalhada de cada página e funcionalidade da aplicação.
    """)

    st.header("Funcionalidades da Aplicação")

    st.subheader("1. Buscar Contatos")
    st.markdown("""
    Na página **Buscar Contatos**, você pode fornecer o nome de uma cidade e buscar automaticamente os contatos de imobiliárias que vendem terrenos na região. Esses contatos incluem o número de celular e o e-mail das imobiliárias. Você também pode adicionar esses contatos diretamente à tabela de contatos da aplicação.
    """)

    st.subheader("2. Contatos")
    st.markdown("""
    Na página **Contatos**, você pode visualizar os contatos que foram salvos na aplicação. Aqui, você tem a opção de:
    - **Baixar a lista de contatos**: Baixe um arquivo CSV contendo todos os contatos armazenados (compatível com Excel e outros editores de planilhas).
    - **Enviar mensagens automaticamente**: Envie mensagens para os contatos de forma automática via WhatsApp, usando as credenciais configuradas na página de **Configuração da API**.
    """)

    st.subheader("3. Definir Mensagens")
    st.markdown("""
    Na página **Definir Mensagens**, você pode configurar a mensagem que será enviada via WhatsApp para os contatos das imobiliárias. Isso permite que você personalize o conteúdo antes de disparar as mensagens automaticamente.
    """)

    st.subheader("4. Envio Automático")
    st.markdown("""
    A página **Envio Automático** combina a funcionalidade de buscar contatos e enviar mensagens em um único passo. 
    Aqui, ao fornecer o nome de uma cidade, a aplicação buscará os contatos das imobiliárias e enviará a mensagem automaticamente para os números de WhatsApp encontrados.
    """)

    st.subheader("5. Configuração da API")
    st.markdown("""
    Na página **Configuração da API**, você pode inserir suas credenciais do **Z-API** (que é utilizado para o envio de mensagens via WhatsApp). Certifique-se de ter uma conta no Z-API e configurar as credenciais corretamente para garantir que o envio automático de mensagens funcione.
    """)

    st.subheader("6. Importar Contatos")
    st.markdown("""
    Na página **Importar Contatos**, você pode fazer upload de um arquivo CSV com uma lista de contatos, caso tenha feito um backup ou recebido uma lista de contatos externa. Isso facilita a restauração de contatos ou o compartilhamento de dados.
    """)

    st.header("Considerações de Segurança")
    st.markdown("""
    A aplicação **não** armazena os dados de forma permanente online. Por isso, é **altamente recomendado** que você faça backups periódicos baixando o arquivo CSV da página de **Contatos**.

    A aplicação não tem critérios de login ou autenticação, portanto, **não compartilhe** o link da aplicação com pessoas não autorizadas.

    Nós **não nos responsabilizamos** por eventuais perdas de dados. Por isso, sempre mantenha uma cópia local dos contatos importantes para evitar qualquer imprevisto.
    """)

    st.header("Dúvidas e Suporte")
    st.markdown("""
    Se você tiver qualquer dúvida sobre o uso da aplicação ou encontrar problemas, por favor, entre em contato com o suporte técnico.
    """)

