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
N0 = st.select_slider(
    label="Densidade espectral de potência do ruído $N_0$:",
    options=[0, 0.01, 0.1, 1],
)

pulse = komm.RectangularPulse()
p_t = A * pulse.taps(sps)   # Pulso de transmissão
q_t = np.flip(p_t)          # Pulso de recepção (casado)
awgn = komm.GaussianChannel(noise_power=N0/2 / dt)

# Sistema
u_n = np.array([-1.0, +1.0, +1.0, -3.0])    # Sequência de entrada
u_t = komm.sampling_rate_expand(u_n, factor=sps) / dt
x_t = komm.convolve(p_t, u_t) * dt          # Sinal PAM transmitido
y_t = awgn.transmit(x_t)                    # Canal
v_t = komm.convolve(q_t, y_t) * dt          # Saída do filtro de RX
v_n = komm.sampling_rate_compress(v_t, factor=sps)

st.write("u[n]:", "[" + ", ".join(map(str,u_n)) + "]")
st.write("V[n]:", "[" + ", ".join(f"valor:.1f" for valor in v_n[1:5]) + "]")

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
    ax.set_ylim(-10.5, 10.5)
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
    ax.plot(ts0/1e-6, v_n, 'C2o', label="$v[n]$")
    ax.set_xlabel("$t$ [µs]")
    ax.set_ylabel("$v(t)$ [V]")
    ax.set_ylim(-3.5, 3.5)
    ax.legend()
    ax.grid()
    st.pyplot(fig)
