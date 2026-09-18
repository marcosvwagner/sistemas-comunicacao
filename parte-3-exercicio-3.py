import komm
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.header("parte 3 -- Exercicio 3")

rng = np.random.default_rng(seed=42)
komm.global_rng.set(rng)

# Parâmetros
N0 = 200e-6     # PSD do ruído [V²/Hz]
sps = 50        # Amostras por símbolo (bit, nesse caso)

questao = st.radio(label="Questão:", options=["Letra (a)", "Letra (b)"], horizontal=True)

if questao == "Letra (a)":
    Rb = 10e3               # Taxa de bits [bit/s]
    Tb = 1 / Rb             # Intervalo de bit [s]
    A = np.sqrt(1 / Tb)     # Amplitude de p(t) [sqrt(Hz)]
    B = 2.0                 # Amplitude de x(t) [V]
    Eb = B**2 * Tb          # Energia média de bit [V²s]
    pam = komm.Constellation([-np.sqrt(Eb), np.sqrt(Eb)])   # Polar
    Pb_teo = komm.gaussian_q(np.sqrt(2 * Eb / N0))
    pulse = komm.RectangularPulse(1.0)  # NRZ

else:  # if questao == "Letra (b)":
    Rb = 23.1e3             # Taxa de bits [bit/s]
    Tb = 1 / Rb             # Intervalo de bit [s]
    A = np.sqrt(2 / Tb)     # Amplitude de p(t) [sqrt(Hz)]
    B = 10.0                # Amplitude de x(t) [V]
    Eb = B**2 * Tb / 4      # Energia média de bit [V²s]
    pam = komm.Constellation([0.0, np.sqrt(2*Eb)]) # Unipolar
    Pb_teo = komm.gaussian_q(np.sqrt(Eb / N0))
    pulse = komm.RectangularPulse(0.5)  # RZ

dt = Tb / sps   # Passo de simulação [s]
Ns = 10000      # Número de bits transmitidos

source = komm.DiscreteMemorylessSource(2)
m_n = source.emit(Ns)
u_n = pam.indices_to_symbols(m_n)

# Simulação em tempo contínuo
awgn = komm.GaussianChannel(noise_power=N0/2 / dt)
p_t = A * pulse.taps(sps)   # Filtro de TX
q_t = np.flip(p_t)          # Filtro de RX (casado)
u_t = komm.sampling_rate_expand(u_n, factor=sps) / dt
x_t = np.convolve(p_t, u_t) * dt
y_t = awgn.transmit(x_t)
v_t = np.convolve(y_t, q_t) * dt
v_n = komm.sampling_rate_compress(v_t, factor=sps)
v_n = v_n[1 : Ns+1]         # Compensa atraso
m_n_hat = pam.closest_indices(v_n)  # Demodulação de mínima distância
Pb_sim_ct = np.mean(m_n != m_n_hat)

# Simulação em tempo discreto
awgn = komm.GaussianChannel(noise_power=N0/2)
v_n = awgn.transmit(u_n)
m_n_hat = pam.closest_indices(v_n)
Pb_sim_dt = np.mean(m_n != m_n_hat)

cols = st.columns(3)
with cols[0]:
    st.metric("BER teo", f"{Pb_teo:.2%}")
with cols[1]:
    st.metric("BER sim (ct)", f"{Pb_sim_ct:.2%}")
with cols[2]:
    st.metric("BER sim (dt)", f"{Pb_sim_dt:.2%}")

fig, ax = plt.subplots(figsize=(10, 5))
t = np.arange(x_t.size)*dt
ax.plot(t/1e-3, x_t, label="$x(t)$")
ax.plot(t/1e-3, y_t, label="$y(t)$", alpha=0.5)
ax.set_xlim(0, 16*Tb / 1e-3)
ax.set_ylim(-12, 12)
ax.set_xlabel("$t$ [ms]")
ax.legend()
ax.grid()
st.pyplot(fig)
