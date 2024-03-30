# Aula 2: Importação
import pandas as pd

file = "Cópia de Imersão Python - Tabela de ações.xlsx"

df_principal = pd.read_excel(file, sheet_name="Principal")
df_total_de_acoes = pd.read_excel(file, sheet_name="Total_de_acoes")
df_ticker = pd.read_excel(file, sheet_name="Ticker")
df_chatgpt = pd.read_excel(file, sheet_name="ChatGPT")

print(df_principal.head(10))