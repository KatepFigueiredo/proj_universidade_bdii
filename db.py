import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def db_connection(role=None):
    conn = None # Inicializa conn para garantir que esteja definido
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"), # app_user
            password=os.getenv("DB_PASSWORD"),
            dbname=os.getenv("DB_NAME")
        )
        if role:
            cur = conn.cursor()
            cur.execute(f"SET ROLE {role};") # Define a role para a sessão
            cur.close()
        return conn
    except Exception as e:
        if conn:
            conn.close() # Garante que a conexão seja fechada em caso de erro
        raise # Relança a exceção para ser tratada pela rota Flask