# Aula 4: Análises Avançadas de Ações e Gráficos de Velas
# import pandas as pd
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

# adicionando titulo e rotulos para os eixos x e y
plt.title("Gráfico de candlestic - Petra.SA com matplotlib")
plt.xlabel("Date")
plt.ylabel("Price")

# adicionando uma grade para facilitar a visiualização dos valores
plt.grid(True)

# Criando subplots
"""
"Primeiro, criamos uma figura que conterá nossos gráficos usando make_subplots.
Isso nos permite ter múltiplos gráficos em uma única visualização.
Aqui, teremos dois subplots: um para o gráfico de candlestick e outro para o volume de transações."

"""
fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.1,
    subplot_titles=("Candlesticks", "Volume Transacionado"),
    row_width=[0.2, 0.7],
)

"""
"No gráfico de candlestick, cada candle representa um dia de negociação,
mostrando o preço de abertura, fechamento, máximo e mínimo. Vamos adicionar este gráfico à nossa figura."
"""
# Adicionando o gráfico de candlestick
fig.add_trace(
    go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Candlestick",
    ),
    row=1,
    col=1,
)

# Adicionando as médias móveis
# Adicionamos também médias móveis ao mesmo subplot para análise de tendências
fig.add_trace(
    go.Scatter(x=df.index, y=df["MA7"], mode="lines", name="MA7 - Média Móvel 7 Dias"),
    row=1,
    col=1,
)

fig.add_trace(
    go.Scatter(
        x=df.index, y=df["MA14"], mode="lines", name="MA14 - Média Móvel 14 Dias"
    ),
    row=1,
    col=1,
)

# Adicionando o gráfico de barras para o volume
# Em seguida, criamos um gráfico de barras para o volume de transações, que nos dá uma ideia da atividade de negociação naquele dia
fig.add_trace(go.Bar(x=df.index, y=df["Volume"], name="Volume"), row=2, col=1)

# Atualizando layout
# Finalmente, configuramos o layout da figura, ajustando títulos, formatos de eixo e outras configurações para tornar o gráfico claro e legível.
fig.update_layout(
    yaxis_title="Preço",
    xaxis_rangeslider_visible=False,  # Desativa o range slider
    width=1100,
    height=600,
)

# Mostrando o gráfico
fig.show()

mpf.plot(
    data.head(30),
    type="candle",
    figsize=(16, 8),
    volume=True,
    mav=(7, 14),
    style="yahoo",
)
