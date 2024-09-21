import sqlite3

def create_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
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
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        whatsapp_message TEXT,
        email_message TEXT
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
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    new_contacts = 0
    
    for contacts in contacts_list:
        for celular in contacts['celular']:
            for email in contacts['email']:
                # Verifica se o contato já existe
                if not contact_exists(cursor, celular, email):
                    cursor.execute('''
                    INSERT INTO contacts (site, celular, email, city, mensagens_enviadas) VALUES (?, ?, ?, ?, ?)
                    ''', (contacts['site'], celular, email, city, 0))
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

def update_message_count(db_path, site):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE contacts
    SET mensagens_enviadas = mensagens_enviadas + 1
    WHERE site = ?
    ''', (site,))
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
