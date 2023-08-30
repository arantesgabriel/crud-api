import psycopg2

conn = psycopg2.connect(
    dbname="userdb",
    user="postgres",
    password="root",
    host="localhost"
)

cursor = conn.cursor()

create_table_query = '''
CREATE TABLE tusuario (
    codigo SERIAL PRIMARY KEY NOT NULL,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL 
);
'''

cursor.execute(create_table_query)
conn.commit()

cursor.close()
conn.close()
