import komm
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.header("Parte 3 -- PAM: Curva BER")

rng = np.random.default_rng(seed=42)
komm.global_rng.set(rng)

# Parâmetros
cols = st.columns(2)
with cols[0]:
    M = st.radio(label="Ordem da modulação $M$:", options=[2, 4, 8], horizontal=True)
with cols[1]:
    labeling_choice = st.radio(label="Rotulagem:", options=["Gray", "Natural"], horizontal=True)

Nb = 60_000             # Número de bits transmitidos
k = int(np.log2(M))     # Número de bits por símbolo da modulação

# Faixa de Eb/N0
if M == 2:
    EbN0_dB_list = np.arange(-4, 9)
elif M == 4:
    EbN0_dB_list = np.arange(-4, 11)
else:  # M == 8
    EbN0_dB_list = np.arange(-4, 15)

# Escolha da rotulagem
if labeling_choice == "Gray":
    labeling = komm.ReflectedLabeling(k)
else:  # labeling_choice == "Natural":
    labeling = komm.NaturalLabeling(k)

source = komm.DiscreteMemorylessSource(2)
pam = komm.PAMConstellation(M)

bits = source.emit(Nb)
m_n = labeling.bits_to_indices(bits)
u_n = pam.indices_to_symbols(m_n)
Es = pam.mean_energy()
Eb = Es / k
Pb_teo_gray_high_snr = np.empty(EbN0_dB_list.size)
Pb_sim = np.empty(EbN0_dB_list.size)
for i, EbN0_dB in enumerate(EbN0_dB_list):
    EbN0 = 10**(EbN0_dB / 10)
    N0 = float(Eb / EbN0)
    awgn = komm.GaussianChannel(N0/2)
    v_n = awgn.transmit(u_n)
    m_hat_n = pam.closest_indices(v_n)
    bits_hat = labeling.indices_to_bits(m_hat_n)
    Pb_sim[i] = np.mean(bits != bits_hat)
    Ps_teo = 2*(M-1)/M * komm.gaussian_q(np.sqrt((6 * Es) / ((M**2 - 1) * N0)))
    Pb_teo_gray_high_snr[i] = Ps_teo / k

# Saída
fig, ax = plt.subplots(figsize=(10, 6))
ax.semilogy(EbN0_dB_list, Pb_sim, "C0o-", label=f"Simulação; {labeling_choice}")
ax.semilogy(EbN0_dB_list, Pb_teo_gray_high_snr, f"k--", label=f"Teoria; Gray hard; alta SNR")
ax.set_xlabel("$E_b/N_0$ [dB]")
ax.set_ylabel("$P_b$")
ax.set_ylim(1e-4, 1)
ax.grid(which="both", linestyle=":")
ax.legend()
st.pyplot(fig)
