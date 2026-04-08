from kruskal import executar_kruskal, encontrar_rota

caminho_arquivo = 'datasets/grafoPonderadoMunicipios.csv'
arvore_geradora, todas_cidades = executar_kruskal(caminho_arquivo)

print("=== ROTA DE REDE ELÉTRICA ===")
print(f"Criador de rotas otimizadas para distribuição de energia elétrica no estado de Goiás.\nMunicípios disponíveis: {len(todas_cidades)}")

while True:
    print("\n------------------------------------------------")
    origem_input = input("Digite o município gerador de energia (ou 'sair'): ").strip()
    
    if origem_input.lower() == 'sair':
        break
        
    destino_input = input("Digite o município afastado (destino): ").strip()

    if origem_input not in todas_cidades or destino_input not in todas_cidades:
        print("Erro: Verifique se os nomes dos municípios estão corretos e presentes no arquivo grafoPonderadoMunicipios.")
        continue

    rota = encontrar_rota(arvore_geradora, origem_input, destino_input)

    if rota:
        print(f"\nRota encontrada na malha elétrica (Kruskal) de {origem_input} até {destino_input}:")
        custo_rota = 0.0
        
        for i in range(len(rota)):
            cidade, peso = rota[i]
            if i == 0:
                print(f" -> {cidade} (Origem)")
            else:
                custo_rota += peso
                print(f" -> {cidade} (Trecho: {peso:.2f} km)")
                
        print(f"\nDistância total de cabeamento para este trecho isolado: {custo_rota:.2f} km")
    else:
        print(f"Não foi possível encontrar uma rota entre {origem_input} e {destino_input}.")