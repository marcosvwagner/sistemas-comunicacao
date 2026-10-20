import komm
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.header("Parte 4 -- Exercício 1")

const = komm.Constellation([4j, -2+2j, 2+2j, 1+1j, -2j])
Rs = 50e3       # Taxa de símbolos [símbolos/s = baud]
Ts = 1 / Rs     # Intervalo de símbolo [s]
sps = 500       # Samples per symbol [amostras/símbolo]
dt = Ts / sps   # Passo de simulação [s]

pulse = komm.RectangularPulse()
A = np.sqrt(1 / Ts)
p_t = A * pulse.taps(sps)
m_n = np.array([0, 1, 1, 4, 3])
u_n = const.indices_to_symbols(m_n)
u_t = komm.sampling_rate_expand(u_n, factor=sps) / dt
sbola_t = komm.convolve(u_t, p_t) * dt
t = np.arange(sbola_t.size) * dt

tabs = st.tabs(["Constelação", "Retangular", "Polar", "Banda passante"])

with tabs[0]:
    cols = st.columns(2)
    with cols[0]:
        st.metric(
            label="Média $\\mu_s$:",
            value=f"{const.mean()[0]:g}",
        )
    with cols[1]:
        st.metric(
            label="Energia média $E_s$:",
            value=f"{const.mean_energy():g}",
        )
    fig, ax = plt.subplots()
    ax.plot(np.real(const.matrix), np.imag(const.matrix), "o")
    ax.set_xlabel("Re")
    ax.set_ylabel("Im")
    ax.set_aspect("equal")
    ax.set_xlim(-5, 5)
    ax.grid()
    st.pyplot(fig)

with tabs[1]:
    fig, ax = plt.subplots(2, 1)
    ax[0].plot(t/1e-6, np.real(sbola_t/A))
    ax[0].set_xlabel("$t$ [µs]")
    ax[0].set_ylabel("$x(t)$")
    ax[0].set_ylim(-4.5, 4.5)
    ax[0].grid()
    ax[1].plot(t/1e-6, np.imag(sbola_t/A))
    ax[1].set_xlabel("$t$ [µs]")
    ax[1].set_ylabel("$y(t)$")
    ax[1].set_ylim(-4.5, 4.5)
    ax[1].grid()
    fig.tight_layout()
    st.pyplot(fig)

with tabs[2]:
    fig, ax = plt.subplots(2, 1)
    ax[0].plot(t/1e-6, np.abs(sbola_t/A))
    ax[0].set_xlabel("$t$ [µs]")
    ax[0].set_ylabel(f"$a(t)$")
    ax[0].set_ylim(-0.5, 4.5)
    ax[0].grid()
    ax[1].plot(t/1e-6, np.angle(sbola_t/A) * (180/np.pi))
    ax[1].set_xlabel("$t$ [µs]")
    ax[1].set_ylabel("$\\theta(t)$ [graus]")
    ax[1].set_ylim(-200, 200)
    ax[1].set_yticks(np.arange(-180, 181, 45))
    ax[1].grid()
    fig.tight_layout()
    st.pyplot(fig)

with tabs[3]:
    fc = st.slider(
        label="Frequência da portadora $f_c$:",
        min_value=100.0,
        max_value=1000.0,
        step=1.0,
        value=500.0,
        format="%g kHz",
    ) * 1e3
    s_t = np.real(sbola_t * np.exp(2j * np.pi * fc * t))

    fig, ax = plt.subplots()
    ax.plot(t/1e-6, s_t/A)
    ax.set_xlabel("$t$ [µs]")
    ax.set_ylabel("$s(t)$")
    ax.set_ylim(-5, 5)
    ax.grid()
    st.pyplot(fig)
