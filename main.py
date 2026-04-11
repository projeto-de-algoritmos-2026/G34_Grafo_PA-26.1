from kruskal import executar_kruskal, encontrar_rota as encontrar_rota_kruskal
from prim import executar_prim, encontrar_rota as encontrar_rota_prim

caminho_arquivo = 'datasets/grafoPonderadoMunicipios.csv'

print("=== ROTA DE REDE ELÉTRICA ===")
print("Criador de rotas otimizadas para distribuição de energia elétrica no estado de Goiás.\n")

# Menu de seleção do método
print("Selecione o método para calcular a árvore geradora mínima:")
print("1 - Kruskal")
print("2 - Prim")

while True:
    escolha = input("\nDigite a opção (1 ou 2): ").strip()
    if escolha in ['1', '2']:
        break
    else:
        print("Opção inválida! Digite 1 para Kruskal ou 2 para Prim.")

# Executar o método selecionado
if escolha == '1':
    print("\n✓ Método Kruskal selecionado")
    arvore_geradora, todas_cidades = executar_kruskal(caminho_arquivo)
    encontrar_rota = encontrar_rota_kruskal
    metodo_nome = "Kruskal"
else:
    print("\n✓ Método Prim selecionado")
    arvore_geradora, todas_cidades = executar_prim(caminho_arquivo)
    encontrar_rota = encontrar_rota_prim
    metodo_nome = "Prim"

print(f"Municípios disponíveis: {len(todas_cidades)}")

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
        print(f"\nRota encontrada na malha elétrica ({metodo_nome}) de {origem_input} até {destino_input}:")
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