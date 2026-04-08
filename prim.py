import csv
import heapq

def executar_prim(caminho_csv):
    grafo = {}
    vertices = set()

    with open(caminho_csv, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for linha in reader:
            origem  = linha[0]
            destino = linha[1]
            peso    = float(linha[2])

            vertices.add(origem)
            vertices.add(destino)

            if origem not in grafo: grafo[origem] = []
            if destino not in grafo: grafo[destino] = []

            grafo[origem].append((peso, destino))
            grafo[destino].append((peso, origem))

    inicio = next(iter(vertices))
    visitados = {inicio}
    heap = [(peso, inicio, vizinho) for peso, vizinho in grafo.get(inicio, [])]
    heapq.heapify(heap)
    mst = []

    while heap:
        peso, origem, destino = heapq.heappop(heap)

        if destino in visitados:
            continue

        visitados.add(destino)
        mst.append((origem, destino, peso))

        for prox_peso, prox_vizinho in grafo.get(destino, []):
            if prox_vizinho not in visitados:
                heapq.heappush(heap, (prox_peso, destino, prox_vizinho))

    return mst, vertices

def encontrar_rota(mst, origem, destino):
    adj = {}
    for u, v, peso in mst:
        if u not in adj: adj[u] = []
        if v not in adj: adj[v] = []
        adj[u].append((v, peso))
        adj[v].append((u, peso))

    visitados = {origem}
    fila = [[(origem, 0.0)]]

    while fila:
        caminho = fila.pop(0)
        nodo_atual, _ = caminho[-1]

        if nodo_atual == destino:
            return caminho

        for vizinho, peso in adj.get(nodo_atual, []):
            if vizinho not in visitados:
                visitados.add(vizinho)
                novo_caminho = list(caminho)
                novo_caminho.append((vizinho, peso))
                fila.append(novo_caminho)

    return None