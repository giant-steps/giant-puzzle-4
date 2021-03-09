import numpy as np

# Código para o item c

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

# Dado que faltam n normais para o colecionador, k holográficas, curr_n_album é o número de figurinhas do álbum 
# disponíveis considerando as figurinhas que ele já retirou no pacotinho (como se o universo de figurinhas disponível
# fosse reduzido) e curr_n_hol é o número de holográficas disponíveis considerando o que ele já retirou no dado
# pacotinho, a função abaixo calcula a probabilidade de vir uma normal repetida. Note que p_new é igual ao p do
# código anterior, substituindo o número de figurinhas do álbum por curr_n_album e o número de holográficas por
# curr_n_hol. Dessa forma, a raridade das holográficas é mantida com relação às não-holográficas.
def probRepNorm(n, k, curr_n_album, curr_n_hol):
    p_new = 1.0 / ((curr_n_album - curr_n_hol) + curr_n_hol / ratio)
    return ((curr_n_album - curr_n_hol - n) * p_new)

# Código semelhante ao da função anterior, porém calcula a probabilidade de vir uma holográfica repetida
def probRepHolo(n, k, curr_n_album, curr_n_hol):
    p_new = 1.0 / ((curr_n_album - curr_n_hol) + curr_n_hol / ratio)
    return ((curr_n_hol - k) * p_new / ratio)

# Código semelhante ao da função  anterior, porém calcula a probabilidade de vir uma nova normal
def probNewNorm(n, k, curr_n_album, curr_n_hol):
    p_new = 1.0 / ((curr_n_album - curr_n_hol) + curr_n_hol / ratio)
    return n * p_new

# Código semelhante ao da função  anterior, porém calcula a probabilidade de vir uma nova holográfica
def probNewHolo(n, k, curr_n_album, curr_n_hol):
    p_new = 1.0 / ((curr_n_album - curr_n_hol) + curr_n_hol / ratio)
    return k * p_new / ratio 

# Função que retorna o custo de comprar tudo no mercado paralelo
def parallelMarketCost(n, k):
    return n * normal_price + k * hol_price

# Função recursiva  que calcula a probabilidade de se retirar curr_norm normais e curr_hol 
# holográficas não repetidas em um pacotinho, considerando que curr_n_album é o número de
# figurinhas disponíveis no álbum dado o que já foi retirado e curr_n_hol é o número de holográficas
def probTot(n, k, packet_size, curr_val, curr_norm, curr_hol, curr_n_album, curr_n_hol):
    if curr_norm < 0 or curr_hol < 0:
        return 0.0
    if curr_val == packet_size:
        if curr_norm != 0 or curr_hol != 0:
            return 0.0
        return 1.0
    return probNewNorm(n, k, curr_n_album, curr_n_hol) * probTot(n-1, k, packet_size, curr_val+1, curr_norm-1, curr_hol, curr_n_album-1, curr_n_hol) + probNewHolo(n, k, curr_n_album, curr_n_hol) * probTot(n, k-1, packet_size, curr_val+1, curr_norm, curr_hol-1, curr_n_album-1, curr_n_hol-1) + probRepNorm(n, k, curr_n_album, curr_n_hol) * probTot(n, k, packet_size, curr_val+1, curr_norm, curr_hol, curr_n_album-1, curr_n_hol) + probRepHolo(n, k, curr_n_album, curr_n_hol) * probTot(n, k, packet_size, curr_val+1, curr_norm, curr_hol, curr_n_album-1, curr_n_hol-1)

# O código abaixo funciona de forma semelhante ao anterior, resolvendo a recursão e calculando o valor
# gasto para se comprar tudo no mercado paralelo a cada valor de n normais restantes e k holográficas
shape_0 = int(n_album - n_hol)
shape_1 = int(n_hol)
f = np.zeros((shape_0 + 1 + nb_fig, shape_1 + 1 + nb_fig))
for n in range(0, shape_0 + 1):
    for k in range(0, shape_1 + 1):
        if n == 0 and k == 0:
            continue
        pm = parallelMarketCost(n, k)
        pk = 1.0 / (1.0 - probTot(n, k, nb_fig, 0, 0, 0, n_album, n_hol))
        pz = packet_price
        for r in range(nb_fig+1):
            for s in range(nb_fig+1-r):
                if r == 0 and s == 0:
                    continue
                pz += f[n-r+nb_fig, k-s+nb_fig] * probTot(n, k, nb_fig, 0, r, s, n_album, n_hol)
        pz *= pk
        f[n+nb_fig, k+nb_fig] = min([pm, pz])
    print(n)
print(f[-1, -1])