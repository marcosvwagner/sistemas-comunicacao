import komm
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.header("Root-raised cosine")

rng = np.random.default_rng(seed=42)
komm.global_rng.set(rng)

# Parâmetros
Rs = 1.0        # Taxa de símbolos [baud]
Ts = 1 / Rs     # Intervalo de símbolo [s]
Ns = 400        # Número de símbolos de entrada
sps = 50        # Amostras por símbolo
dt = Ts / sps   # Passo de simulação [s]

cols = st.columns(2)

with cols[0]:
    rolloff = st.slider(
        label="Fator de rolloff ($\\alpha$):",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.01,
    )

with cols[1]:
    N0 = st.select_slider(
        label="Densidade espectral de potência do ruído $N_0$:",
        options=[0, 0.01, 0.1, 1],
    )

pulse = komm.RaisedCosinePulse(rolloff).root()
# pulse = komm.BeaulieuPulse(rolloff).root()
awgn = komm.GaussianChannel(noise_power=N0/2 / dt)

u_n = rng.choice([-3, -1, 1, 3], size=Ns)
p_t = pulse.taps(samples_per_symbol=sps, span=(-16, 16))
q_t = np.flip(p_t)
u_t = komm.sampling_rate_expand(u_n, factor=sps) / dt
x_t = komm.convolve(p_t, u_t) * dt
y_t = awgn.transmit(x_t)
v_t = np.convolve(q_t, y_t) * dt
v_n = komm.sampling_rate_compress(v_t, factor=sps)

tabs = st.tabs([
    "Pulso",
    "Saída do filtro casado",
    "Diagrama de olho",
])

with tabs[0]:  # Pulso
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

    t = np.linspace(-16, 16, num=1000)
    ax[0].plot(t, pulse.waveform(t), label="$p(t)$")
    ax[0].set_xlabel("$t / T_s$")
    ax[0].set_ylim(-0.5, 1.5)
    ax[0].legend()
    ax[0].grid()

    f = np.linspace(-1.5, 1.5, num=1000)
    ax[1].plot(f, pulse.spectrum(f), label="$P(f)$")
    ax[1].set_xlabel("$f / R_s$")
    ax[1].set_ylim(-0.1, 1.1)
    ax[1].legend()
    ax[1].grid()
    st.pyplot(fig)

with tabs[1]:  # Saída do filtro casado
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(np.arange(v_t.size)*dt, v_t, "C0-", label="$v(t)$")
    ax.plot(np.arange(v_n.size)*Ts, v_n, "C1o", label="$v[n]$")
    ax.set_xlabel("$t / T_s$")
    ax.set_ylim(-6, 6)
    ax.legend()
    ax.grid()
    st.pyplot(fig)

with tabs[2]:  # Diagrama de olho
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    scope_width = 3  # Número de símbolos no "osciloscópio"
    Na = scope_width * sps
    t = np.linspace(0.0, scope_width, num=Na + 1)
    for i in range(len(u_n) // scope_width):
        n = np.arange(i*Na, (i+1)*Na + 1)
        ax.plot(t, v_t[n], "C0", alpha=0.25)
    ax.set_xlim(0.0, scope_width)
    ax.set_ylim(-6, 6)
    ax.set_xlabel("$t / T_s$")
    ax.grid()
    st.pyplot(fig)
