def dist(a, b):
    arr = []
    for i in range(min(len(a), len(b))):
        arr.append(a[i] - b[i])
        arr = list(map(lambda x : x * x, arr))
    return sum(arr) ** (1/2)

arq_lista = open("iris.data", "r")
linhas = list(map(lambda linha : linha.replace("\n", ""), arq_lista.readlines()))
linhas = list(map(lambda linha: linha.split(','), linhas))

classe_1 = linhas[4]
classe_2 = linhas[60]
classe_3 = linhas[120]

exemplo_1 = linhas[5]
exemplo_2 = linhas[6]
exemplo_3 = linhas[61]
exemplo_4 = linhas[62]
exemplo_5 = linhas[121]
exemplo_6 = linhas[122]


return (exemplo_1,   exemplo_2,  exemplo_3,  exemplo_4,  exemplo_5,  exemplo_6)
