import komm
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.header("Parte 2 -- Exercício 4")

rng = np.random.default_rng(seed=42)
komm.global_rng.set(rng)

# Parâmetros
Rs = 50e3               # Taxa de símbolos [símbolos/s = baud]
Ts = 1 / Rs             # Intervalo de símbolo [s]
sps = 100               # Amostras por símbolo
dt = Ts / sps           # Passo de simulação [s]
A = np.sqrt(1 / Ts)     # Amplitude de p(t) [sqrt(Hz)]
span=(-5,5)

col1, col2 = st.columns(2)

with col1:
    alpha = st.slider(
        label= "Fator de roll-off $\\alpha$:",
        min_value= 0.0,
        max_value= 1.0,
        step=0.2
    )

with col2:
    N0 = st.select_slider(
    label="Densidade espectral de potência do ruído $N_0$:",
    options=[0, 0.01, 0.1, 1],
    )
    
rc = komm.RaisedCosinePulse(rolloff= alpha)
pulse = rc.root()
p_t = A * pulse.taps(sps,span)   # Pulso de transmissão
q_t = np.flip(p_t)          # Pulso de recepção (casado)
awgn = komm.GaussianChannel(noise_power=N0/2 / dt)

# Sistema
u_n = np.array([0.7, 1.4, 0.8, -0.5])    # Sequência de entrada
u_t = komm.sampling_rate_expand(u_n, factor=sps) / dt
x_t = komm.convolve(p_t, u_t) * dt          # Sinal PAM transmitido
y_t = awgn.transmit(x_t)                    # Canal
v_t = komm.convolve(q_t, y_t) * dt          # Saída do filtro de RX

# Atrasos 
delay_filter= (len(p_t)- 1) //2
delay_total = 2 * delay_filter

# Instantes de coleta
coleta_indices = (delay_total + np.arange(len(u_n)) * sps)
v_n = v_t[coleta_indices]
coleta_tempo = coleta_indices * dt

# v_n = komm.sampling_rate_compress(v_t, factor=sps)

col1,col2 = st.columns(2)

with col1:
    st.write("u[n]:", "[" + ", ".join(map(str,u_n)) + "]")

with col2:
    st.write(f"V[n]: [{', '.join(f'{valor:.1f}' for valor in v_n[0:5])}]")
tabs = st.tabs([
    "Sinal PAM $x(t)$",
    "Pulso equivalente $h(t)$",
    "Sinal $v(t)$"
])

with tabs[0]:
    fig, ax = plt.subplots(figsize=(6, 3))
    ts = np.arange(x_t.size) * dt
    ax.plot(ts/1e-6, y_t/A, "C3", label="$y(t) / A$")
    ax.plot(ts/1e-6, x_t/A, "C0", label="$x(t) / A$")
    ax.set_xlabel("$t$ [µs]")
    ax.set_ylim(-4.5, 4.5)
    ax.legend()
    ax.grid()
    st.pyplot(fig)

with tabs[1]:
    h_t = komm.convolve(p_t, q_t) * dt
    fig, ax = plt.subplots(figsize=(6, 3))
    ts = np.arange(h_t.size) * dt
    ax.plot(ts/1e-6, h_t)
    ax.set_xlabel("$t$ [µs]")
    ax.set_ylabel("$h(t)$")
    ax.grid()
    st.pyplot(fig)

with tabs[2]:
    fig, ax = plt.subplots(figsize=(6, 3))
    ts = np.arange(v_t.size) * dt
    ts0 = np.arange(v_n.size) * Ts
    ax.plot(ts/1e-6, v_t, 'C2-', label="$v(t)$")
    ax.plot(coleta_tempo/1e-6, v_n, 'C2o', label="$v[n]$")
    ax.set_xlabel("$t$ [µs]")
    ax.set_ylabel("$v(t)$ [V]")
    ax.set_ylim(-2.0, 2.0)
    # ax.set_xlim(150,300)
    ax.legend()
    ax.grid()
    st.pyplot(fig)
