import sqlite3
from sqlite3 import Error
import csv
import os
import shutil

BD_CADASTROS = 'cadastros.db'


def create_connection():
    conexao = sqlite3.connect(BD_CADASTROS)
    return conexao


def sql_companhias(conn):
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS companhias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                CNPJ_CIA VARCHAR(20),
                DT_REG DATE,
                DENOM_SOCIAL VARCHAR(100),
                SIT CHAR(80),
                DT_INI_SIT DATE
            )
        ''')


def inserir_dados(conn, data):
    with conn:
        for entry in data:
            cnpj = entry[0]
            existing_record = conn.execute("SELECT * FROM companhias WHERE CNPJ_CIA = ?", (cnpj,)).fetchone()
            if existing_record:
                conn.execute('''
                    UPDATE companhias
                    SET DT_REG=?, DENOM_SOCIAL=?, SIT=?, DT_INI_SIT=?
                    WHERE CNPJ_CIA=?
                ''', (entry[1], entry[2], entry[3], entry[4], cnpj))
                print(f"Registro atualizado para CNPJ {cnpj}")
            else:
                conn.execute('''
                    INSERT INTO companhias (CNPJ_CIA, DT_REG, DENOM_SOCIAL, SIT, DT_INI_SIT) 
                    VALUES (?, ?, ?, ?, ?)
                ''', entry)
                print(f"Novo registro inserido para CNPJ {cnpj}")


def load_csv_data(conn, csv_directory):
    if not os.path.exists(csv_directory):
        print(f"Erro: Diretório {csv_directory} não encontrado.")
        return

    for filename in os.listdir(csv_directory):
        if filename.endswith('.csv'):
            filepath = os.path.join(csv_directory, filename)
            print(f"Lendo o arquivo {filename}")

            with open(filepath, 'r', encoding='ISO-8859-1') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                header = next(reader, None)
                if header is None:
                    print(f"Aviso: Arquivo {filename} não contém cabeçalho.")
                    continue

                column_indices = get_column_indices(header)

                try:
                    first_row = next(reader)
                except StopIteration:
                    print(f"Aviso: Arquivo {filename} não contém dados após o cabeçalho.")
                    continue

                num_columns = len(header)
                if len(first_row) != num_columns:
                    print(f"Erro: Número de colunas inconsistente no arquivo {filename}")
                    continue

                data = []
                for row in [first_row] + list(reader):
                    if len(row) != num_columns:
                        print(f"Erro: Número de colunas inconsistente na linha do arquivo {filename}")
                        continue

                    relevant_data = [row[i] for i in column_indices]

                    data.append(relevant_data)

            # Inserir os dados na tabela
            try:
                inserir_dados(conn, data)
            except Error as e:
                print(f"Erro ao inserir dados do arquivo {filename}: {e}")
                continue

            # Mover o arquivo para indicar que foi processado
            processado_directory = os.path.join(csv_directory, "processado")
            if not os.path.exists(processado_directory):
                os.makedirs(processado_directory)
            shutil.move(filepath, os.path.join(processado_directory, filename))
            print(f"Arquivo {filename} movido para {processado_directory}")

    print("Todos os arquivos foram processados com sucesso.")


def get_column_indices(header):
    # Nomes das colunas da tabela
    companhias_columns = ['CNPJ_CIA', 'DT_REG', 'DENOM_SOCIAL', 'SIT', 'DT_INI_SIT']

    column_indices = []
    for column_name in companhias_columns:
        try:
            index = header.index(column_name)
            column_indices.append(index)
        except ValueError:
            print(f"Erro: Coluna '{column_name}' não encontrada no cabeçalho do CSV.")

    return column_indices


def main():
    conn = create_connection()
    sql_companhias(conn)

    load_csv_data(conn, 'data')

    conn.close()


if __name__ == '__main__':
    main()
