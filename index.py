import requests
import mysql.connector
from mysql.connector import Error

# Configuração do banco de dados
import os

DB_CONFIG = {
    "host": os.getenv('DB_HOST', 'localhost'),
    "user": os.getenv('DB_USER', 'root'),
    "password": os.getenv('DB_PASSWORD', '1234'),
    "database": os.getenv('DB_NAME', 'cnae_db')
}

# URL base da API
BASE_URL = "http://servicodados.ibge.gov.br/api/v2/cnae/divisoes"

# Criação da tabela se não existir
CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS CNAE (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(10) UNIQUE NOT NULL,
    apelido TEXT NOT NULL,
    descricao TEXT NOT NULL,
    ramo TEXT NOT NULL,
    anotacao TEXT
);
"""

# Função para conectar ao banco
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

# Função para criar a tabela CNAE
def create_table():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(CREATE_TABLE_QUERY)
        conn.commit()
        cursor.close()
        conn.close()
        print("Tabela CNAE criada ou já existente.")

# Função para buscar todas as divisões CNAE e suas subclasses
def get_all_cnaes():
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        divisoes = response.json()

        conn = get_db_connection()
        if not conn:
            return
        
        cursor = conn.cursor()

        for divisao in divisoes:
            divisao_id = divisao["id"]
            descricao_divisao = divisao["descricao"]
            print(f"Buscando subclasses para divisão {divisao_id}: {descricao_divisao}")

            # Obtém as subclasses da divisão
            subclasses_url = f"http://servicodados.ibge.gov.br/api/v2/cnae/divisoes/{divisao_id}/subclasses"
            sub_response = requests.get(subclasses_url)
            sub_response.raise_for_status()
            subclasses = sub_response.json()

            for cnae in subclasses:
                codigo = str(cnae["id"])
                descricao = cnae["descricao"]
                grupo = cnae["classe"]["grupo"]["divisao"]["descricao"]
                anotacao = "".join(cnae.get("observacoes", []))

                # Verifica se já existe
                cursor.execute("SELECT codigo FROM CNAE WHERE codigo = %s", (codigo,))
                if cursor.fetchone():
                    print(f"CNAE {codigo} já existe.")
                else:
                    cursor.execute("""
                        INSERT INTO CNAE (codigo, apelido, descricao, ramo, anotacao)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (codigo, descricao, descricao, grupo, anotacao))
                    print(f"CNAE {codigo} cadastrado.")

        conn.commit()
        cursor.close()
        conn.close()
    except requests.RequestException as e:
        print(f"Erro ao buscar dados da API: {e}")
    except Error as e:
        print(f"Erro ao inserir no banco de dados: {e}")

# Formata os códigos CNAE no banco
def formatar_cnaes():
    conn = get_db_connection()
    if not conn:
        return

    cursor = conn.cursor()
    cursor.execute("SELECT id, codigo FROM CNAE")
    cnaes = cursor.fetchall()

    for cnae_id, codigo in cnaes:
        if len(codigo) == 7:
            novo_codigo = f"{codigo[:4]}-{codigo[4]}/{codigo[5:]}"
            cursor.execute("UPDATE CNAE SET codigo = %s WHERE id = %s", (novo_codigo, cnae_id))
            print(f"CNAE formatado: {novo_codigo}")

    conn.commit()
    cursor.close()
    conn.close()

# Execução do script
if __name__ == "__main__":
    create_table()
    get_all_cnaes()
    formatar_cnaes()