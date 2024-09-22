import streamlit as st
import pandas as pd
import os

from utils import import_contacts_from_csv

def process_csv_file(db_path, csv_file):
    df = pd.read_csv(csv_file, sep=',')
    df.columns = [col.lower() for col in df.columns]
    contacts_list = df.to_dict(orient='records')
    return import_contacts_from_csv(db_path, contacts_list)

def run():
    st.header("Importar Contatos")
    db_path = os.path.join('data', 'contacts.sqlite')
    
    # Instruções detalhadas para o usuário
    st.subheader("Como importar contatos via CSV")
    st.markdown("""
    ### Estrutura do Arquivo CSV
    Para importar contatos, você precisa de um arquivo CSV com as seguintes colunas:

    - **Site**: O site relacionado ao contato.
    - **Celular**: O número de telefone do contato.
    - **Email**: O email do contato.
    - **Cidade**: A cidade onde o contato está localizado.
    - **Mensagens Enviadas**: O número de mensagens enviadas (geralmente 0 ao adicionar um novo contato).

    Exemplo de linha em um arquivo CSV:
    ```
    https://www.exemplo.com,(12) 3456-7890,contato@exemplo.com,São Paulo,0
    ```

    ### Propósito dessa página
    Esta página permite que você reimporte contatos salvos anteriormente. A importação é útil, por exemplo, quando você fez um backup local do banco de dados e deseja restaurar ou compartilhar esses contatos com outra pessoa.

    ### Como criar o CSV
    Você pode exportar a tabela de contatos atual através da **página de contatos**. 
    Na página de contatos, há um botão para **baixar** a tabela de contatos no formato CSV. Essa funcionalidade é importante por vários motivos:

    - **Segurança**: Nós não nos responsabilizamos por eventuais perdas de dados. O banco de dados online pode sofrer falhas ou exclusões, então recomendamos que você faça **backups frequentes** clicando no botão de download da tabela.
    - **Compatibilidade**: O arquivo CSV baixado pode ser aberto no Excel, Google Sheets ou outro editor de planilhas para revisão ou compartilhamento.
    - **Restauração rápida**: Se você precisar restaurar seus contatos, basta carregar o arquivo CSV novamente nesta página e o banco de dados será populado automaticamente.

    ### Instruções para Importar o CSV:
    1. Baixe o CSV da página de contatos.
    2. Faça as edições que desejar (opcional).
    3. Carregue o arquivo CSV aqui e clique no botão de upload.
    """)

    # Upload do arquivo CSV
    csv_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

    if csv_file is not None:
        num_contacts_imported = process_csv_file(db_path, csv_file)
        st.success(f"{num_contacts_imported} contatos importados com sucesso!")
