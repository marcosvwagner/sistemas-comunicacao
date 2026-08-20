import komm
import matplotlib.pyplot as plt
import numpy as np 
import streamlit as st

st.header("parte 1 - exercicio")

dt = 1e-6    # Passo de tempo continuo [s]
fa = 8.0     # Taxa de amostragem [amostras/s]
ta = 1/fa    # Periodo de amostragem [s]
L = 16        # Nº de nivels de quantização
delta = 1.0  # Passo de quantizaçao [v]
t0 = 0.0     # Tempo inicial do intervalo de simulação [s]
tf = 2.0     # Tempo final de simulação [s]

# Mensagem
ts = np.arange(t0,tf, step=dt)
x_t = 5.0 * np.sin(2*np.pi*ts)

# Amostragem
x_n = komm.sampling_rate_compress(x_t, int(ta/dt))
ns = np.arange(x_n.size)

# Quantização
quant = komm.UniformQuantizer.mid_riser(num_levels=L, step=delta)
d_n = quant.digitize(x_n)
y_n = quant.quantize(x_n)

# Recomposição do sinal (X_hat)

xhat_t = np.zeros_like(x_t)
for n in ns:
    xhat_t += y_n[n] * np.sinc((ts-n*ta -t0)/ ta)


tabs = st.tabs((["Curva entrada x saida", "Sinais", "Tabela"]))

with tabs[0]:
    entrada = np.linspace(-10, 10, num=10000)
    saida = quant.quantize(entrada)
    fig, ax = plt.subplots(figsize=(8,6))
    ax.plot(entrada, saida)
    ax.set_xlabel("$x$ [V]")
    ax.set_ylabel("$y$ [V]")
    ax.set_xticks(quant.thresholds)
    ax.set_yticks(quant.levels)
    ax.grid()
    st.pyplot(fig)

with tabs[1]:
    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(ts/1e-3,x_t,"C0",label="$x(t)$")
    ax.plot((ns*ta)/1e-3,x_n,"C2o",label="$x(n)$")
    ax.plot((ns*ta)/1e-3,y_n,"C1o",label="$y(n)$")

    ax.plot(ts/1e-3,xhat_t,"C3",label="$xhat_t(t)$")

    ax.grid()
    ax.set_xlabel("$t$ [ms]")
    ax.legend()
    st.pyplot(fig)

with tabs[2]:
    st.table({
        "$x[n]$":x_n,
        "$d[n]$":d_n,
        "$y[n]$":y_n, 
    })
