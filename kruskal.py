import csv

class UnionFind:
    def __init__(self, vertices):
        self.pai = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, item):
        if self.pai[item] == item:
            return item
        self.pai[item] = self.find(self.pai[item])
        return self.pai[item]

    def union(self, x, y):
        xroot = self.find(x)
        yroot = self.find(y)

        if xroot != yroot:
            if self.rank[xroot] < self.rank[yroot]:
                self.pai[xroot] = yroot
            elif self.rank[xroot] > self.rank[yroot]:
                self.pai[yroot] = xroot
            else:
                self.pai[yroot] = xroot
                self.rank[xroot] += 1

def executar_kruskal(caminho_csv):
    arestas = []
    vertices = set()

    with open(caminho_csv, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for linha in reader:
            origem = linha[0]
            destino = linha[1]
            peso = float(linha[2])
            
            arestas.append((origem, destino, peso))
            vertices.add(origem)
            vertices.add(destino)

    arestas.sort(key=lambda x: x[2])
    
    uf = UnionFind(vertices)
    mst = []

    for origem, destino, peso in arestas:
        if uf.find(origem) != uf.find(destino):
            uf.union(origem, destino)
            mst.append((origem, destino, peso))

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