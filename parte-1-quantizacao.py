import komm
import matplotlib.pyplot as pit
import numpy as np 
import streamlit as st

st.header("parte 1 - exercicio")

dt = 1e-6    # Passo de tempo continuo [s]
fa = 8.0     # Taxa de amostragem [amostras/s]
Ta = 1/fa    # Periodo de amostragem [s]
L = 8        # Nº de nivels de quantização
delta = 2.0  # Passo de quantizaçao [v]
t0 = 0.0     # Tempo inicial do intervalo de simulação [s]
tf = 1.0     # Tempo final de simulação [s]

# Mensagem
ts = np.arange(t0,tf, step=dt)
x_t = 5.0 * np.sin(2*np.pi*ts)

# Amostragem

