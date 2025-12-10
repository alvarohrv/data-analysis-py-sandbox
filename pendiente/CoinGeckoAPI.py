# -*- coding: utf-8 -*-
"""
Pendiente de comprender.

bitcoin_chart.ipynb

Original file is located at
    https://colab.research.google.com/drive/1ySEqbaChu96kqvhzNo9nIDyxnrLoLK5P
"""

'''
!pip install pandas pycoingecko plotly
'''

import pandas as pd
from pycoingecko import CoinGeckoAPI
import plotly.graph_objects as go

# 1. Descargar datos de mercado de Bitcoin (30 días)
cg = CoinGeckoAPI() # Crear instancia de la API de CoinGecko

# Obtener datos de mercado de Bitcoin para los últimos 30 días
bitcoin_data = cg.get_coin_market_chart_by_id( 
    id='bitcoin',
    vs_currency='usd',
    days=30
)

# 2. Construir un DataFrame a partir de la lista de precios
# bitcoin_data['prices'] es una lista de [timestamp_ms, price]
# la data original no tiene columnas, así que las definimos aquí:
data = pd.DataFrame(bitcoin_data['prices'], columns=['TimeStamp', 'Price'])

# 3. Convertir el timestamp (ms) a fecha
# Por defecto, el timestamp está en milisegundos, así que usamos unit='ms'
data['Date'] = pd.to_datetime(data['TimeStamp'], unit='ms')

# 4. Agrupar por día para obtener OHLC (open, high, low, close)
# Resamplear los datos por día y calcular los valores OHLC
candlestick_data = data.resample('1D', on='Date')['Price'].agg(
    first='first',
    max='max',
    min='min',
    last='last'
)

# 5. Crear la figura de velas
fig = go.Figure(
    data=[
        go.Candlestick(
            x=candlestick_data.index,
            open=candlestick_data['first'],
            high=candlestick_data['max'],
            low=candlestick_data['min'],
            close=candlestick_data['last']
        )
    ]
)

fig.update_layout(
    xaxis_rangeslider_visible=False,
    xaxis_title='Date',
    yaxis_title='Price (USD $)',
    title='Bitcoin Candlestick Chart Over Past 30 Days'
)

fig.show()