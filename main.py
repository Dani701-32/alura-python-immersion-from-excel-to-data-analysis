# Aula 2: Importação
from turtle import left
import pandas as pd

file = "Cópia de Imersão Python - Tabela de ações.xlsx"

df_principal = pd.read_excel(file, sheet_name="Principal")
df_total_de_acoes = pd.read_excel(file, sheet_name="Total_de_acoes")
df_ticker = pd.read_excel(file, sheet_name="Ticker")
df_chatgpt = pd.read_excel(file, sheet_name="ChatGPT")

# Aula 03: Manipulação de Dados e Criação de Gráficos com bibliotecas Python
df_principal = df_principal[["Ativo", "Data", "Último (R$)", "Var. Dia (%)"]].copy()
df_principal = df_principal.rename(
    columns={"Último (R$)": "last_value", "Var. Dia (%)": "var_day_percent"}
).copy()

df_principal["var_percent"] = df_principal["var_day_percent"] / 100

df_principal["var_start"] = df_principal["last_value"] / (
    df_principal["var_percent"] + 1
)
df_principal = df_principal.merge(
    df_total_de_acoes, left_on="Ativo", right_on="Código", how="left"
)

df_principal = df_principal.drop(columns=["Código"])

df_principal["var_rs"] = (
    df_principal["last_value"] - df_principal["var_start"]
) * df_principal["Qtde. Teórica"]

pd.options.display.float_format = (
    "{:.2f}".format
)  # Formata os float removemnto a notação científica

df_principal["Qtde. Teórica"] = df_principal["Qtde. Teórica"].astype(int)

df_principal = df_principal.rename(columns={"Qtde. Teórica": "qtd_theory"}).copy()

df_principal["result"] = df_principal["var_rs"].apply(
    lambda x: "Subiu" if x > 0 else ("Desceu" if x < 0 else "Manteve")
)

df_principal = df_principal.merge(
    df_ticker, left_on="Ativo", right_on="Ticker", how="left"
)
df_principal = df_principal.drop(columns=["Ticker"])

df_principal = df_principal.merge(
    df_chatgpt, left_on="Nome", right_on="Nome da Empresa", how="left"
)
df_principal = df_principal.drop(columns=["Nome da Empresa"])

df_principal = df_principal.rename(columns={"Idade (em anos)": "age"}).copy()

df_principal['age_detail'] = df_principal["age"].apply(
    lambda x: "Mais de 100" if x > 100 else ("Menos de 50" if x < 50 else "Entre 100 e 50")
)

print(df_principal.head(10))
