import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from engine import AeroCellEngine
import time

# Configuração da Interface
st.set_page_config(page_title="AeroCell", layout="wide")

st.title("AeroCell 🌬️")

# --- BARRA LATERAL ---
st.sidebar.header("Configurações")
diff_rate = st.sidebar.slider("Difusão", 0.0, 1.0, 0.2)
decay_rate = st.sidebar.slider("Decaimento", 0.001, 0.05, 0.005)
steps = st.sidebar.number_input("Passos", 10, 1000, 200)

# Inicialização do Motor
if 'engine' not in st.session_state:
    # Criamos o motor 50x50
    st.session_state.engine = AeroCellEngine(width=50, height=50, diffusion=diff_rate, decay=decay_rate)
    # Adicionamos a barreira central
    st.session_state.engine.add_obstacle(20, 10, 22, 40)

# Sincroniza parâmetros
st.session_state.engine.diffusion = diff_rate
st.session_state.engine.decay = decay_rate

if st.sidebar.button("🚀 Liberar Contaminação"):
    st.session_state.engine.emit(10, 25, 10.0)

if st.sidebar.button("🧹 Resetar"):
    st.session_state.engine.grid[:] = 0
    st.rerun()

# --- ÁREA DE EXIBIÇÃO CENTRALIZADA ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    plot_spot = st.empty()

# Loop da Simulação
for i in range(steps):
    st.session_state.engine.update()
    
    # Criamos a figura compacta para evitar scroll
    fig, ax = plt.subplots(figsize=(5, 5))
    
    # --- LÓGICA DE VISUALIZAÇÃO CORRIGIDA ---
    # 1. Pegamos a grade de contaminação pura (valores >= 0)
    data = np.copy(st.session_state.engine.grid)
    
    # 2. Criamos uma máscara para o que é ZERO (Ar Limpo -> Branco)
    # Usamos um threshold muito baixo para considerar ar limpo
    data_masked = np.ma.masked_where(data < 0.0001, data)
    
    # 3. Desenhamos a contaminação (Amarelo -> Vermelho)
    im = ax.imshow(data_masked, 
                   cmap="YlOrRd", 
                   vmin=0.001, 
                   vmax=1.0, 
                   interpolation='nearest',
                   origin='upper',
                   zorder=2) # Fica por cima
    
    # 4. Desenhamos os OBSTÁCULOS separadamente (Cinza)
    # Criamos uma máscara onde 1 é obstáculo e 0 é transparente
    obs_mask = np.ma.masked_where(st.session_state.engine.obstacles == 0, st.session_state.engine.obstacles)
    ax.imshow(obs_mask, cmap="binary", vmin=0, vmax=1.5, interpolation='nearest', origin='upper', zorder=3)
    
    # Fundo branco para as células vazias
    ax.set_facecolor("white")
    
    # --- GRADE E ESTÉTICA ---
    ax.set_xticks(np.arange(-0.5, 50, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, 50, 1), minor=True)
    ax.grid(which='minor', color='black', linestyle='-', linewidth=0.1, alpha=0.1)
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"Passo: {i} | AeroCell", fontsize=10)
    
    plot_spot.pyplot(fig)
    plt.close(fig)
    
    if np.max(st.session_state.engine.grid) < 0.0001 and i > 5:
        break
        
    time.sleep(0.01)