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

    csv_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

    if csv_file is not None:
        num_contacts_imported = process_csv_file(db_path, csv_file)
        st.success(f"{num_contacts_imported} contatos importados com sucesso!")
