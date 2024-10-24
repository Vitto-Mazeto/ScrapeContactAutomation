import sqlite3

def create_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Criação da tabela 'contacts'
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site TEXT,
        celular TEXT,
        email TEXT,
        city TEXT,
        mensagens_enviadas INTEGER DEFAULT 0
    )
    ''')

    # Criação da tabela 'messages'
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        whatsapp_message TEXT,
        email_message TEXT
    )
    ''')

    # Criação da tabela 'zapi_config'
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS zapi_config (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        instance_id TEXT,
        token TEXT,
        api_url TEXT
    )
    ''')

    # Criação da tabela 'zyte_config'
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS zyte_config (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        token TEXT
    )
    ''')

    conn.commit()
    conn.close()

def contact_exists(cursor, celular, email):
    cursor.execute('''
    SELECT 1 FROM contacts WHERE celular = ? OR email = ?
    ''', (celular, email))
    return cursor.fetchone() is not None

def save_contacts_to_db(db_path, contacts_list, city):
    print(f"Salvando os seguintes contatos no banco de dados: {contacts_list}")
    new_contacts = 0

    # Lista para armazenar os valores dos contatos que serão inseridos em lote
    batch_values = []

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Itera sobre os contatos
        for contact in contacts_list:
            # Para cada celular do contato
            for celular in contact['celular']:
                # Verifica se há emails disponíveis; se não, utiliza string vazia
                email = contact['email'][0] if contact['email'] else ""
                
                # Adiciona uma nova linha na lista de batch_values com os dados a serem inseridos
                batch_values.append((contact['site'], celular, email, city, 0))
                new_contacts += 1

        # Se houver valores a inserir, faça o batch insert
        if batch_values:
            cursor.executemany(''' 
                INSERT INTO contacts (site, celular, email, city, mensagens_enviadas) 
                VALUES (?, ?, ?, ?, ?)
            ''', batch_values)
    print(f"{new_contacts} novos contatos adicionados no banco.")
    return new_contacts

def get_current_links(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT site FROM contacts")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

def import_contacts_from_csv(db_path, contacts_list):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    new_contacts = 0

    for contacts in contacts_list:
        celular = contacts['celular']  # Obter celular como string
        email = contacts['email']      # Obter email como string
        city = contacts['cidade']      # Obter cidade diretamente do contato

        # Verifica se o contato já existe
        if not contact_exists(cursor, celular, email):
            cursor.execute('''INSERT INTO contacts (site, celular, email, city, mensagens_enviadas) VALUES (?, ?, ?, ?, ?)''', 
                           (contacts['site'], celular, email, city, 0))
            new_contacts += 1  # Conta como novo contato adicionado

    conn.commit()
    conn.close()
    return new_contacts

def fetch_all_contacts(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_message_count(db_path, phone):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE contacts
    SET mensagens_enviadas = mensagens_enviadas + 1
    WHERE celular = ?
    ''', (phone,))
    conn.commit()
    conn.close()

def delete_all_contacts(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts")
    conn.commit()
    conn.close()

def save_messages(db_path, whatsapp_message, email_message):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM messages
    ''')
    cursor.execute('''
    INSERT INTO messages (whatsapp_message, email_message) VALUES (?, ?)
    ''', (whatsapp_message, email_message))
    conn.commit()
    conn.close()

def fetch_messages(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT whatsapp_message, email_message FROM messages ORDER BY id DESC LIMIT 1
    ''')
    row = cursor.fetchone()
    conn.close()
    return row if row else ("", "")

# Função para salvar dados da API no banco de dados
def save_api_data(db_path, instance_id, token, api_url):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Cria a tabela caso ela não exista
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS zapi_config (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        instance_id TEXT,
        token TEXT,
        api_url TEXT
    )
    ''')

    # Deleta os dados existentes e insere os novos
    cursor.execute('''
    DELETE FROM zapi_config
    ''')
    cursor.execute('''
    INSERT INTO zapi_config (instance_id, token, api_url) 
    VALUES (?, ?, ?)
    ''', (instance_id, token, api_url))
    
    conn.commit()
    conn.close()

# Função para buscar os dados da API no banco de dados
def fetch_api_data(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT instance_id, token, api_url FROM zapi_config ORDER BY id DESC LIMIT 1
    ''')
    row = cursor.fetchone()
    conn.close()
    return row if row else ("", "", "")

# Função para salvar o token da Zyte API no banco de dados
def save_zyte_token(db_path, token):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Cria a tabela caso ela não exista
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS zyte_config (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        token TEXT
    )
    ''')

    # Deleta os dados existentes e insere o novo token
    cursor.execute('''
    DELETE FROM zyte_config
    ''')
    cursor.execute('''
    INSERT INTO zyte_config (token) 
    VALUES (?)
    ''', (token,))
    
    conn.commit()
    conn.close()

# Função para buscar o token da Zyte API no banco de dados
def fetch_zyte_token(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT token FROM zyte_config ORDER BY id DESC LIMIT 1
    ''')
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else ""