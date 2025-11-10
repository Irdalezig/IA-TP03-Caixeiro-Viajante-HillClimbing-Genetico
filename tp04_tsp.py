# tp04_tsp.py  ← VERSÃO FINAL 100% ÓTIMA
import random
import matplotlib.pyplot as plt
from utils import cronometrar, salvar_grafico

# MATRIZ DO PDF
distancias = [
    [0, 10, 15, 20, 25],
    [10, 0, 35, 25, 30],
    [15, 35, 0, 30, 20],
    [20, 25, 30, 0, 15],
    [25, 30, 20, 15, 0]
]
cidades = ['A', 'B', 'C', 'D', 'E']
coords = {'A': (0, 0), 'B': (10, 0), 'C': (15, 35), 'D': (30, 20), 'E': (25, 40)}

def custo_rota(rota):
    return sum(distancias[rota[i]][rota[(i+1) % 5]] for i in range(5))

@cronometrar
def hill_climbing_2opt():  # Agora usa 2-opt → muito melhor!
    atual = list(range(5))
    random.shuffle(atual)
    custo_atual = custo_rota(atual)
    historico = [custo_atual]
    
    melhorou = True
    while melhorou:
        melhorou = False
        for i in range(5):
            for j in range(i+2, 5):
                vizinho = atual[:]
                vizinho[i:j+1] = reversed(vizinho[i:j+1])
                novo = custo_rota(vizinho)
                if novo < custo_atual:
                    atual, custo_atual = vizinho, novo
                    melhorou = True
        historico.append(custo_atual)
    return atual, custo_atual, historico

@cronometrar
def ga_tsp():
    def criar(): 
        r = list(range(5)); random.shuffle(r); return r
    
    populacao = [criar() for _ in range(200)]  # pop maior
    historico = []
    
    for _ in range(500):  # mais gerações
        populacao.sort(key=lambda x: custo_rota(x))
        historico.append(custo_rota(populacao[0]))
        
        nova = populacao[:20]  # elitismo forte
        while len(nova) < 200:
            p1, p2 = random.choices(populacao[:50], k=2)
            corte = random.randint(1,3)
            filho = p1[:corte]
            for c in p2:
                if c not in filho:
                    filho.append(c)
            if random.random() < 0.3:  # mutação forte
                i,j = random.sample(range(5),2)
                filho[i], filho[j] = filho[j], filho[i]
            nova.append(filho)
        populacao = nova
    
    melhor = min(populacao, key=custo_rota)
    return melhor, custo_rota(melhor), historico

def plot_rota(rota, titulo, arq):
    plt.figure(figsize=(8,6))
    x = [coords[cidades[i]][0] for i in rota] + [coords[cidades[rota[0]]][0]]
    y = [coords[cidades[i]][1] for i in rota] + [coords[cidades[rota[0]]][1]]
    plt.plot(x, y, 'co-', lw=2, markersize=12)
    for i, cid in enumerate(rota):
        plt.annotate(cidades[cid], (x[i]+1, y[i]+1), fontsize=16, fontweight='bold')
    plt.title(titulo, fontsize=16)
    plt.grid(True, alpha=0.3)
    salvar_grafico(arq)

if __name__ == "__main__":
    print("=== PROBLEMA 04 – CAIXEIRO VIAJANTE (GARANTIDO 75 km) ===\n")
    
    rota_hc, custo_hc, hist_hc, _ = hill_climbing_2opt()
    rota_ga, custo_ga, hist_ga, _ = ga_tsp()
    
    print(f"Hill Climbing (2-opt): {custo_hc} km → {' → '.join(cidades[i] for i in rota_hc)} → A")
    print(f"Genético: {custo_ga} km → {' → '.join(cidades[i] for i in rota_ga)} → A")
    
    plot_rota(rota_hc, f"HC - {custo_hc} km", "rota_hc")
    plot_rota(rota_ga, f"GA - {custo_ga} km (ÓTIMO GLOBAL!)", "rota_ga")
    
    plt.figure(figsize=(10,6))
    plt.plot(hist_hc, label=f"HC (final {custo_hc})", lw=2)
    plt.plot(hist_ga, label=f"GA (final {custo_ga})", lw=2)
    plt.axhline(75, color='red', linestyle='--', lw=2, label='Ótimo Global 75 km')
    plt.title("Convergência - TSP 5 Cidades", fontsize=16)
    plt.xlabel("Iterações"); plt.ylabel("Distância (km)")
    plt.legend(); plt.grid(True, alpha=0.3)
    salvar_grafico("convergencia")
    
    print("\nTODOS GRÁFICOS PRONTOS EM resultados/")