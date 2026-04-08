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

municipios = []
with open('datasets/municipios.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['codigo_uf'] == '52':
            municipios.append({
                'nome': row['nome'],
                'lat': float(row['latitude']),
                'lon': float(row['longitude'])
            })

arestas = []
distancia_maxima_km = 50.0 # define a distancia maxima para considerar um caminho entre 2 municipios

for m1, m2 in itertools.combinations(municipios, 2):
    distancia = calcular_haversine(m1['lat'], m1['lon'], m2['lat'], m2['lon'])
    
    if distancia <= distancia_maxima_km:
        arestas.append([m1['nome'], m2['nome'], round(distancia, 2)])

with open('datasets/grafoPonderadoMunicipios.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['origem', 'destino', 'peso'])
    writer.writerows(arestas)