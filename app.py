import streamlit as st
import folium
from streamlit_folium import st_folium
from kruskal import executar_kruskal
from prim import executar_prim
from transformardados import carregar_coordenadas, gerar_grafo_ponderado

st.set_page_config(page_title="GO - Distribuição de Rede", layout="wide")

@st.cache_data
def carregar_coords():
    return carregar_coordenadas()

ALGORITMOS = {
    "Kruskal": executar_kruskal,
    "Prim": executar_prim,
}

@st.cache_data
def gerar_e_executar_algoritmo(distancia_maxima_km, algoritmo):
    caminho_grafo = gerar_grafo_ponderado(distancia_maxima_km)
    mst, vertices = ALGORITMOS[algoritmo](caminho_grafo)
    return mst, sorted(list(vertices))

coordenadas = carregar_coords()

if 'pagina' not in st.session_state:
    st.session_state.pagina = 'principal'

def mudar_pagina(nova_pagina):
    st.session_state.pagina = nova_pagina

if st.session_state.pagina == 'principal':
    st.title("Distribuição de Rede Elétrica em Goiás")

    algoritmo = st.radio("Escolha o algoritmo para geração da Árvore Geradora Mínima:", list(ALGORITMOS.keys()), horizontal=True)

    distancia_maxima = st.slider(
        "Distância máxima para conexão entre municípios (km):",
        min_value=50,
        max_value=500,
        value=100,
        step=10
    )

    arvore_geradora, lista_cidades = gerar_e_executar_algoritmo(float(distancia_maxima), algoritmo)

    st.info(f"Grafo gerado com {len(arvore_geradora)} arestas na Árvore Geradora Mínima para {len(lista_cidades)} municípios conectados.")

    origem = st.selectbox("Selecione o município de origem (nó raiz da Árvore Geradora Mínima):", lista_cidades)

    if st.button("Gerar Árvore Geradora Mínima"):
        st.session_state.origem = origem
        st.session_state.mst = arvore_geradora
        st.session_state.algoritmo = algoritmo
        mudar_pagina('mapa')
        st.rerun()

elif st.session_state.pagina == 'mapa':
    origem = st.session_state.origem
    mst = st.session_state.mst
    algoritmo = st.session_state.algoritmo

    st.button("Nova consulta", on_click=mudar_pagina, args=('principal',))

    mapa = folium.Map(location=coordenadas[origem], zoom_start=7)

    custo_total = 0.0
    cidades_na_mst = set()

    for u, v, peso in mst:
        if u in coordenadas and v in coordenadas:
            folium.PolyLine(
                [coordenadas[u], coordenadas[v]],
                color="blue",
                weight=2,
                opacity=0.6,
                tooltip=f"{u} ↔ {v}: {peso:.2f} km"
            ).add_to(mapa)
            custo_total += peso
            cidades_na_mst.add(u)
            cidades_na_mst.add(v)

    for cidade in cidades_na_mst:
        if cidade not in coordenadas:
            continue
        if cidade == origem:
            folium.Marker(
                coordenadas[cidade],
                popup=f"Origem: {cidade}",
                icon=folium.Icon(color="green", icon="bolt", prefix="fa")
            ).add_to(mapa)
        else:
            folium.CircleMarker(
                coordenadas[cidade],
                radius=5,
                color="blue",
                fill=True,
                fill_opacity=0.7,
                popup=cidade
            ).add_to(mapa)

    st.success(f"Árvore Geradora Mínima gerada com {len(mst)} conexões | Algoritmo: {algoritmo} | Nó de origem: {origem}")
    st.metric(label="Custo Total da Árvore Geradora Mínima (km)", value=f"{custo_total:.2f}")

    st_folium(mapa, width=1000, height=500)
