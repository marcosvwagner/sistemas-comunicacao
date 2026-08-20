import komm
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.header("Parte 2 -- Exercício 1")

# Parâmetros
Rs = 50e3       # Taxa de símbolos [símbolos/s = baud]
Ts = 1 / Rs     # Intervalo de símbolo [s]
sps = 100       # Amostras por símbolo
dt = Ts / sps   # Passo de simulação [s]
A = 500.0       # Amplitude de p(t) [sqrt(Hz)

# Pulso
class MeuPulso(komm.Pulse):
    def waveform(self, t):
        t = np.asarray(t)
        return (t - 0.2) / 0.3 * ((0.2 <= t) & (t < 0.5)) + \
               (0.8 - t) / 0.3 * ((0.5 <= t) & (t < 0.8))

# Entrada
u_n = np.array([0.4, -0.1, -0.5, 0.8, -0.2])

# Geração do sinal PAM
pulse = MeuPulso()
u_t = komm.sampling_rate_expand(u_n, factor=sps) / dt
p_t = A * pulse.taps(samples_per_symbol=sps, span=(0, 1))
x_t = komm.convolve(p_t, u_t) * dt

tabs = st.tabs(["Pulso", "Sinal PAM"])

with tabs[0]:
    t = np.arange(p_t.size) * dt
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t/1e-6, A * pulse.waveform(t/Ts))
    ax.set_xlabel("$t$ [µs]")
    ax.set_ylabel("$p(t)$")
    ax.set_xticks(np.arange(0, 22, 2))
    ax.grid()
    st.pyplot(fig)

with tabs[1]:
    t = np.arange(x_t.size) * dt
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t/1e-6, x_t)
    ax.set_xlabel("$t$ [µs]")
    ax.set_ylabel("$x(t)$")
    ax.grid()
    st.pyplot(fig)


st.header("Parte 2 -- Exercício 1 - quadrado")

# Parâmetros
Rs = 50e3       # Taxa de símbolos [símbolos/s = baud]
Ts = 1 / Rs     # Intervalo de símbolo [s]
sps = 100       # Amostras por símbolo
dt = Ts / sps   # Passo de simulação [s]
A = 500.0       # Amplitude de p(t) [sqrt(Hz)

# Pulso
class MeuPulso(komm.Pulse):
    def waveform(self, t):
        t = np.asarray(t)
        return ((0.2 <= t) & (t < 0.8))

# Entrada
u_n = np.array([0.4, -0.1, -0.5, 0.8, -0.2])

# Geração do sinal PAM
pulse = MeuPulso()
u_t = komm.sampling_rate_expand(u_n, factor=sps) / dt
p_t = A * pulse.taps(samples_per_symbol=sps, span=(0, 1))
x_t = komm.convolve(p_t, u_t) * dt

tabs = st.tabs(["Pulso", "Sinal PAM"])

with tabs[0]:
    t = np.arange(p_t.size) * dt
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t/1e-6, A * pulse.waveform(t/Ts))
    ax.set_xlabel("$t$ [µs]")
    ax.set_ylabel("$p(t)$")
    ax.set_xticks(np.arange(0, 22, 2))
    ax.grid()
    st.pyplot(fig)

with tabs[1]:
    t = np.arange(x_t.size) * dt
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t/1e-6, x_t)
    ax.set_xlabel("$t$ [µs]")
    ax.set_ylabel("$x(t)$")
    ax.grid()
    st.pyplot(fig)

