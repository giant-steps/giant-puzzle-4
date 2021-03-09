import numpy as np

# Código para os itens a e b

#Inicialização dos parâmetros do problema. ratio é a razão de raridade entre as figurinhas holográficas e normais
ratio = 5.0

# n_album é a quantidade de figurinhas do álbum
n_album = 680.0

# n_hol é a quantidade de holográficas do álbum
n_hol = 80.0

# packet_price é o preço de cada pacote
packet_price = 0.4

# normal_price é o preço da figurinha normal no mercado paralelo
normal_price = 0.3

# hol_price é o preço da holográfica no mercado paralelo
hol_price = 2.0

# nb_fig é o número de figurinhas por pacote
nb_fig = 7

# p é a probabilidade de uma figurinha selecionada aleatoriamente ser normal
p = 1.0 / ((n_album - n_hol) + n_hol / ratio)

# A função abaixo calcula a probabilidade de uma figurinha selecionada aleatoriamente ser
# normal, dado que faltam n normais e k holográficas
def probRep(n, k):
    return (1.0 - (ratio * n + k) * p / ratio)

# A função abaixo retorna a probabilidade de uma figurinha aleatória ser uma normal que a
# pessoa ainda não possui, dado que faltam n normais e k holográficas
def probNewNorm(n, k):
    return n * p

# A função abaixo retorna a probabilidade de uma figurinha aleatória ser uma holográfica 
# que a pessoa ainda não possui, dado que faltam n normais e k holográficas
def probNewHolo(n, k):
    return k * p / ratio 

# A função abaixo retorna o custo para completar o álbum usando apenas o mercado paralelo,
# dado que faltam n normais e k holográficas
def parallelMarketCost(n, k):
    return n * normal_price + k * hol_price

# A função abaixo retorna a probabilidade de retirar curr_norm normais não repetidas e 
# curr_hol holográficas não repetidas em um pacotinho de figurinhas, dado que faltam n 
# normais e k holográficas
def probTot(n, k, packet_size, curr_val, curr_norm, curr_hol):
    if curr_norm < 0 or curr_hol < 0:
        return 0.0
    if curr_val == packet_size:
        if curr_norm != 0 or curr_hol != 0:
            return 0.0
        return 1.0
    return probNewNorm(n, k) * probTot(n-1, k, packet_size, curr_val+1, curr_norm-1, curr_hol) + probNewHolo(n, k) * probTot(n, k-1, packet_size, curr_val+1, curr_norm, curr_hol-1) + probRep(n, k) * probTot(n, k, packet_size, curr_val+1, curr_norm, curr_hol)

# Quantidade de figurinhas normais e holográficas no álbum, respectivamente
shape_0 = int(n_album - n_hol)
shape_1 = int(n_hol)

# f é a matriz que possui o custo para completar o álbum. f[n, k] é o custo quando faltam n-nb_fig normais 
# e k-nb_fig holográficas
f = np.zeros((shape_0 + 1 + nb_fig, shape_1 + 1 + nb_fig))
for n in range(0, shape_0 + 1):
    for k in range(0, shape_1 + 1):
        if n == 0 and k == 0:
            continue
            
        # Cálculo do custo para comprar n figurinhas normais e k holográficas no mercado paralelo
        pm = parallelMarketCost(n, k)
        
        # Cálculo do custo para completar o álbum caso a pessoa opte por comprar mais um pacote de figurinhas usando recursão
        pk = 1.0 / (1.0 - (probRep(n, k) ** (1.0 * nb_fig)))
        pz = packet_price
        for r in range(nb_fig+1):
            for s in range(nb_fig+1-r):
                if r == 0 and s == 0:
                    continue
                pz += f[n-r+nb_fig, k-s+nb_fig] * probTot(n, k, nb_fig, 0, r, s)
        pz *= pk
        
        # A pessoa optará aqui pela solução que possuir menor valor esperado de custo naquele instante
        f[n+nb_fig, k+nb_fig] = min([pm, pz])
print(f[-1, -1])