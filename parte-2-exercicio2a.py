import komm
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.header("Parte 2 -- Exercício 2")

# Aleatoridade

rng = np.random.default_rng(seed= 42)
komm.global_rng.set(rng=rng)

# Parametros

sps = 50        # Amostras por simbolo
rs = 50e3       # Taxa de simbolos
ts = 1/rs       # Intervalo de simbolos
dt = ts/sps     # Passo de simulação
ns = 100        # Nº de simbolos de entrada
dur = ns*ts     # Duração do sinal
n_iters = 1000  # Numero de iterações

letter = st.radio(
    label="Questão",
    options=["Letra (a)",  "Letra (b)"],
    horizontal=True
)

if letter == "Letra (a)":
    
    a = np.sqrt(1/ts)
    u_n = rng.uniform (low=-3.0, high= 3.0, size=(n_iters, ns))
    pulse = komm.RectangularPulse()
    span = (-1,1)
    psd_teo_densidade = lambda f: 3.0* np.sinc(ts*f)**2

else:
    a = np.sqrt(1/ts)
    alfa_n = rng.normal (loc=0, scale=1, size = (n_iters, ns+1))
    u_n= alfa_n[:,1:] + alfa_n[:,:-1]
    pulse= komm.SincPulse()
    span = (-16,16)
    psd_teo_densidade = lambda f: 4.0 * np.cos(np.pi*ts*f)**2 *(np.abs(ts*f) <=0.5)


    pulse = komm.RectangularPulse()
    span = (-1,1)
    psd_teo_densidade = lambda f: 3.0* np.sinc(ts*f)**2

# Geração de sinal PAM

u_t = komm.sampling_rate_expand(u_n, factor=sps)/dt
p_t = a * pulse.taps(samples_per_symbol=sps, span=span)
x_t = komm.convolve(p_t, u_t) * dt

# Densidade espectral de potencias
x_f, f = komm.fourier_transform(x_t, time_step=dt)
psd_teo = psd_teo_densidade(f)
psd_sim = np.mean(np.abs(x_f)**2,axis=0) /dur

tabs = st.tabs(["Pulso", "Sinal PAM", "PSD"])

with tabs[0]:
    t = np.linspace(-16*ts, 16*ts, num=1000)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t/1e-6, a * pulse.waveform(t/ts))
    ax.set_xlabel("$t~[\\text{µs}]$")
    ax.set_ylabel("$p(t)~[\\sqrt{\\text{Hz}}]$")
    ax.grid()
    st.pyplot(fig)

with tabs[1]:
    t = np.arange(x_t[0].size) * dt
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t/1e-3, x_t[0])
    ax.set_xlabel("$t$ [ms]")
    ax.set_ylabel("$x(t)$ [V]")
    ax.grid()
    st.pyplot(fig)

with tabs[2]:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(f/1e3, psd_sim, "C0", label="Simulado")
    ax.plot(f/1e3, psd_teo, "C1--", label="Teórico")
    ax.set_xlabel("$f$ [kHz]")
    ax.set_ylabel("$S_x(f)$ [V²/Hz]")
    ax.set_xlim(-2*rs/1e3, 2*rs/1e3)
    ax.grid()
    ax.legend()
    st.pyplot(fig)


