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
    conn.commit()
    conn.close()

def save_contacts_to_db(db_path, contacts_list, city):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for contacts in contacts_list:
        for celular in contacts['celular']:
            for email in contacts['email']:
                cursor.execute('''
                INSERT INTO contacts (site, celular, email, city, mensagens_enviadas) VALUES (?, ?, ?, ?, ?)
                ''', (contacts['site'], celular, email, city, 0))
    
    conn.commit()
    conn.close()

def fetch_all_contacts(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_message_count(db_path, contact_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE contacts
    SET mensagens_enviadas = mensagens_enviadas + 1
    WHERE id = ?
    ''', (contact_id,))
    conn.commit()
    conn.close()
