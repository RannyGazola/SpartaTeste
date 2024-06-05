import sqlite3
from sqlite3 import Error
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import subprocess

BD_CADASTROS = 'cadastros.db'

def create_connection():
    conexao = sqlite3.connect(BD_CADASTROS)
    return conexao

def procurar_data(data_pesq, text_widget):
    try:
        con = create_connection()
        cursor = con.cursor()
        query = "SELECT * FROM companhias WHERE DT_INI_SIT = ?"
        cursor.execute(query, (data_pesq,))
        result = cursor.fetchall()

        if result:
            for linha in result:
                text_widget.insert(tk.END, f"CNPJ: {linha[1]}\n")
                text_widget.insert(tk.END, f"Denominação Social: {linha[3]}\n")
                text_widget.insert(tk.END, f"Situação: {linha[4]}\n")
                dt_reg = datetime.strptime(linha[2], "%Y-%m-%d")
                text_widget.insert(tk.END, f"Data de registro: {dt_reg.strftime('%d/%m/%Y')}\n")
                dt_ini_sit = datetime.strptime(linha[5], "%Y-%m-%d")
                text_widget.insert(tk.END, f"Data de início da situação: {dt_ini_sit.strftime('%d/%m/%Y')}\n\n")
        else:
            text_widget.insert(tk.END, f"Nenhum registro encontrado para a data: {data_pesq}\n")

    except Error as e:
        text_widget.insert(tk.END, f"Erro ao conectar ao SQLite: {e}\n")
    finally:
        if con:
            cursor.close()
            con.close()

def on_search_click(entry, text_widget):
    text_widget.delete(1.0, tk.END)
    data_para_pesquisar = entry.get()
    try:
        data_convertida = datetime.strptime(data_para_pesquisar, "%d/%m/%Y").strftime("%Y-%m-%d")
        procurar_data(data_convertida, text_widget)
    except ValueError:
        text_widget.insert(tk.END, "Formato de data inválido. Use DD/MM/AAAA.\n")

def run_atualizar_script():
    try:
        subprocess.run(["python", "atualizar.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script atualizar.py: {e}")

def main():
    janela = tk.Tk()
    janela.title("Teste Sparta - Pesquisa")
    janela.configure(bg='black')

    frame_pesquisa = tk.Frame(janela, bg='black')
    frame_pesquisa.pack(padx=10, pady=10)

    entry_label = tk.Label(frame_pesquisa, text="Digite a data (DD/MM/AAAA):", fg='white', bg='black')
    entry_label.pack(anchor='w')

    entry = tk.Entry(frame_pesquisa, width=20)
    entry.pack(anchor='w')

    search_button = tk.Button(frame_pesquisa, text="Pesquisar", command=lambda: on_search_click(entry, text_widget))
    search_button.pack(anchor='w', pady=5)

    resultados_frame = tk.Frame(janela, bg='black')
    resultados_frame.pack(padx=10, pady=(0, 10), fill='both', expand=True)

    text_widget = tk.Text(resultados_frame, wrap='word', bg='black', fg='white')
    text_widget.pack(side='left', fill='both', expand=True)

    scroll_bar = ttk.Scrollbar(resultados_frame, command=text_widget.yview)
    scroll_bar.pack(side='right', fill='y')

    text_widget.config(yscrollcommand=scroll_bar.set)

    frame_botoes = tk.Frame(janela, bg='black')
    frame_botoes.pack(pady=5)

    atualizar_button = tk.Button(frame_botoes, text="Atualizar", command=run_atualizar_script)
    atualizar_button.pack(side='left', padx=5)

    close_button = tk.Button(frame_botoes, text="Fechar", command=janela.quit)
    close_button.pack(side='left', padx=5)

    janela.mainloop()


if __name__ == '__main__':
    main()
