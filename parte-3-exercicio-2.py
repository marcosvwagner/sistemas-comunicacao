import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.header("parte 3 -- Exercicio 2")

M = 4
us = np.array([1-3.0, -1.0, +1.0, +3.0])
priors = np.array([0.1,0.2,0.3,0.4])

cols = st.columns(2)

with cols[0]:
    v = st.slider(
        label="Ponto recebido $v$:",
        min_value=-4.0,
        max_value=4.0,
        value=1.5,
        step=0.01,
    )

with cols[1]:
    logN0 = st.select_slider(
        label="Densidade espectral de potência do ruído $N_0$:",
        options=np.linspace(-2.0, 3.0, num=2000),
        format_func=lambda x: f"{10**x:.3f}"
    )
    N0 = 10**logN0

posteriors = np.exp(-(v -us)**2 / N0) * priors
posteriors /= np.sum(posteriors)


fig, ax = plt.subplots(figsize=(10,5))
ax.bar(us, priors, width=0.8, label="a priori")
ax.bar(us, posteriors, width=0.4, label="a posteriori")
ax.plot(v, 0, "C3o", label="recebido")
ax.set_ylabel("Probabilidade")
ax.set_xlim(-4, 4)
ax.set_ylim(-0.1, 1.1)
ax.grid()
ax.legend()
st.pyplot(fig)

