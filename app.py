import streamlit as st
import folium
from streamlit_folium import st_folium
import unicodedata
import time
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


def chave_ordenacao_cidade(cidade):
    texto_normalizado = unicodedata.normalize("NFKD", cidade)
    texto_sem_acento = "".join(caractere for caractere in texto_normalizado if not unicodedata.combining(caractere))
    return texto_sem_acento.casefold()

def gerar_caminho_grafo(distancia_maxima_km):
    caminho_grafo = gerar_grafo_ponderado(distancia_maxima_km)
    return caminho_grafo


def gerar_e_executar_algoritmo(distancia_maxima_km, algoritmo):
    caminho_grafo = gerar_caminho_grafo(distancia_maxima_km)
    inicio = time.perf_counter()
    mst, vertices = ALGORITMOS[algoritmo](caminho_grafo)
    tempo_execucao = time.perf_counter() - inicio
    return mst, sorted(list(vertices), key=chave_ordenacao_cidade), tempo_execucao

def filtrar_componente(mst, origem):
    adj = {}
    for u, v, peso in mst:
        adj.setdefault(u, []).append((v, peso))
        adj.setdefault(v, []).append((u, peso))

    visitados = {origem}
    fila = [origem]
    arestas = []

    while fila:
        atual = fila.pop(0)
        for vizinho, peso in adj.get(atual, []):
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append(vizinho)
                arestas.append((atual, vizinho, peso))

    return arestas

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

    arvore_geradora, lista_cidades, tempo_execucao = gerar_e_executar_algoritmo(float(distancia_maxima), algoritmo)

    st.info(f"Grafo gerado com {len(arvore_geradora)} arestas na Árvore Geradora Mínima para {len(lista_cidades)} municípios conectados.")

    origem = st.selectbox("Selecione o município de origem (nó raiz da Árvore Geradora Mínima):", lista_cidades)

    if st.button("Gerar Árvore Geradora Mínima"):
        st.session_state.origem = origem
        st.session_state.mst = arvore_geradora
        st.session_state.algoritmo = algoritmo
        st.session_state.tempo_execucao = tempo_execucao
        mudar_pagina('mapa')
        st.rerun()

elif st.session_state.pagina == 'mapa':
    origem = st.session_state.origem
    mst = st.session_state.mst
    algoritmo = st.session_state.algoritmo
    tempo_execucao = st.session_state.tempo_execucao

    st.button("Nova consulta", on_click=mudar_pagina, args=('principal',))

    arestas_origem = filtrar_componente(mst, origem)
    vertices_origem = {cidade for u, v, _ in arestas_origem for cidade in (u, v)} | {origem}
    arestas_isoladas = [(u, v, p) for u, v, p in mst if u not in vertices_origem or v not in vertices_origem]

    mapa = folium.Map(location=coordenadas[origem], zoom_start=7)

    for u, v, peso in arestas_isoladas:
        if u in coordenadas and v in coordenadas:
            folium.PolyLine(
                [coordenadas[u], coordenadas[v]],
                color="blue",
                weight=2,
                opacity=0.5,
                tooltip=f"{u} ↔ {v}: {peso:.2f} km"
            ).add_to(mapa)

    for u, v, peso in arestas_origem:
        if u in coordenadas and v in coordenadas:
            folium.PolyLine(
                [coordenadas[u], coordenadas[v]],
                color="red",
                weight=2.5,
                opacity=0.8,
                tooltip=f"{u} ↔ {v}: {peso:.2f} km"
            ).add_to(mapa)

    cidades_isoladas = {cidade for u, v, _ in arestas_isoladas for cidade in (u, v)}
    cidades_isoladas -= vertices_origem

    for cidade in cidades_isoladas:
        if cidade in coordenadas:
            folium.CircleMarker(
                coordenadas[cidade],
                radius=4,
                color="blue",
                fill=True,
                fill_opacity=0.6,
                popup=cidade
            ).add_to(mapa)

    for cidade in vertices_origem:
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
                radius=4,
                color="red",
                fill=True,
                fill_opacity=0.7,
                popup=cidade
            ).add_to(mapa)

    legenda_html = """
    <div style="position: fixed; bottom: 30px; left: 30px; z-index: 1000;
                background-color: white; color: black; padding: 12px 16px; border-radius: 8px;
                border: 1px solid #ccc; font-size: 13px; line-height: 1.8;">
        <b>Legenda</b><br>
        <span style="color: red; font-size: 18px;">&#9644;</span> Componente do nó de origem<br>
        <span style="color: blue; font-size: 18px;">&#9644;</span> Componentes isolados<br>
        <span style="color: green; font-size: 16px;">&#9679;</span> Nó de origem
    </div>
    """
    mapa.get_root().html.add_child(folium.Element(legenda_html))

    custo_origem = sum(p for _, _, p in arestas_origem)
    custo_total = sum(p for _, _, p in mst)

    st.success(f"Algoritmo: {algoritmo} | Nó de origem: {origem}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Custo do componente de origem (km)", f"{custo_origem:.2f}")
    col2.metric("Custo total da floresta geradora (km)", f"{custo_total:.2f}")
    col3.metric("Tempo de execução", f"{tempo_execucao:.4f} s")

    st_folium(mapa, width=1000, height=500)
