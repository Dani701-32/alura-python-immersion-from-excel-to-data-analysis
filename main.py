# Aula 4: Análises Avançadas de Ações e Gráficos de Velas
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.dates as mdates
import mplfinance as mpf
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

data = yf.download("PETR4.SA", start="2023-01-01", end="2023-12-31")  # petrobras 2023
data["Close"].plot(figsize=(10, 6))
plt.title("Variation by date", fontsize=16)
plt.legend(["Close"])

df = data.head(60).copy()
# Convertedo o indice em uma coluna de data
df["Date"] = df.index
# Convertendo as datas para o formato numérico de matplotlib
# Isso é necessário para que o matplotlib possa plotar as datas corretamente no gráfico
df["Date"] = df["Date"].apply(mdates.date2num)
fig, ax = plt.subplots(figsize=(15, 8))
# Vamos definir a largura dos candles no gráfico
width = 0.7

for i in range(len(df)):
    # Determinando a cor docandle
    # Se o preço de fechamento for maior que o de abertura, o candle é verde
    # se for menor, o candle é vermelho
    if df["Close"].iloc[i] > df["Open"].iloc[i]:
        color = "green"
    else:
        color = "red"

    # Desenha a linha vetical do candle
    # Essa linha mostra os preços máximo( topo da linha) e mínimo (base da linha) do dia.
    # Usamos 'ax.plot' para desenhar uma linha vertical.
    # [df["Data"].iloc[i], df["Data"].iloc[i]] define o ponto x da linha (a data) e [df["low"].iloc[i], df["High"].iloc[i]] define a altura do canlde
    ax.plot(
        [df["Date"].iloc[i], df["Date"].iloc[i]],
        [df["Low"].iloc[i], df["High"].iloc[i]],
        color=color,
        linewidth=1,
    )
    ax.add_patch(
        patches.Rectangle(
            (
                df["Date"].iloc[i] - width / 2,
                min(df["Open"].iloc[i], df["Close"].iloc[i]),
            ),
            width,
            abs(df["Close"].iloc[i] - df["Open"].iloc[i]),
            facecolor=color,
        )
    )
df["MA7"] = df["Close"].rolling(window=7).mean()
df["MA14"] = df["Close"].rolling(window=14).mean()

# Plotanto as médias móveis
ax.plot(
    df["Date"], df["MA7"], color="orange", label="Média Móvel 7 dias"
)  # Média de 7 dias
ax.plot(
    df["Date"], df["MA14"], color="yellow", label="Média Móvel 14 dias"
)  # Média de 14 dias
# adicionar legendas para as médias
ax.legend()

# formatando o eixo x para mostrar as datas
# Configuramos o formato da adata e a toração para melhor legibilidade
ax.xaxis_date()  # O Método é usado para dizer ao matplotlib que as datas estão sendo usadas no eixo x
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
plt.xticks(rotation=45)

#adicionando titulo e rotulos para os eixos x e y
plt.title("Gráfico de candlestic - Petra.SA com matplotlib")
plt.xlabel("Date")
plt.ylabel("Price")

#adicionando uma grade para facilitar a visiualização dos valores
plt.grid(True)
plt.show()
