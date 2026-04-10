import csv
import math
import itertools

def calcular_haversine(lat1, lon1, lat2, lon2):
    raio_terra = 6371.0
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return raio_terra * c

def carregar_municipios(caminho_csv='datasets/municipios.csv', codigo_uf='52'):
    municipios = []
    with open(caminho_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['codigo_uf'] == codigo_uf:
                municipios.append({
                    'nome': row['nome'],
                    'lat': float(row['latitude']),
                    'lon': float(row['longitude'])
                })
    return municipios

def carregar_coordenadas(caminho_csv='datasets/municipios.csv', codigo_uf='52'):
    coords = {}
    for m in carregar_municipios(caminho_csv, codigo_uf):
        coords[m['nome']] = [m['lat'], m['lon']]
    return coords

def gerar_grafo_ponderado(distancia_maxima_km, caminho_entrada='datasets/municipios.csv', caminho_saida='datasets/grafoPonderadoMunicipios.csv'):
    municipios = carregar_municipios(caminho_entrada)
    arestas = []
    for m1, m2 in itertools.combinations(municipios, 2):
        distancia = calcular_haversine(m1['lat'], m1['lon'], m2['lat'], m2['lon'])
        if distancia <= distancia_maxima_km:
            arestas.append([m1['nome'], m2['nome'], round(distancia, 2)])

    with open(caminho_saida, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['origem', 'destino', 'peso'])
        writer.writerows(arestas)

    return caminho_saida
