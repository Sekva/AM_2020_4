arq_lista = open("car.data", "r")
linhas = arq_lista.readlines()

# remove \n no final
linhas = list(map(lambda linha : linha.replace("\n", ""), linhas))

# separa pelas virgulas
linhas = list(map(lambda linha: linha.split(','), linhas))

def predizer(atr):

    predicao = None

    if atr[0] == "vhigh" and atr[1] == "vhigh":
        predicao = "unacc"

    if atr[0] == "vhigh" and atr[1] == "high":
        predicao = "unacc"

    if atr[0] == "high" and atr[1] == "vhigh":
        predicao = "unacc"

    if atr[0] == "med" and atr[1] == "med" and atr[2] == "2" and atr[3] == "2":
        predicao = "unacc"

    if (atr[2] == "4" or atr[2] == "5more") and (atr[3] == "4" or atr[3] == "more"):
        predicao = "acc"

    if (atr[0] == "med" or atr[0] == "low") and (atr[3] == "4" or atr[3] == "more") and atr[5] == "high":
        predicao = "vgood"

    if (atr[0] == "med" or atr[0] == "low") and (atr[1] == "med" or atr[1] == "low") and atr[5] == "high":
        predicao = "good"

    if atr[5] == "low":
        predicao = "unacc"

    return (predicao, atr)

predicoes = list(map(predizer, linhas))

funcao_checagem = lambda predicao : 1 if predicao[0] == predicao[1][6] else 0

from functools import reduce
numero_acertos = reduce(lambda a, b : a + b, map(funcao_checagem, predicoes))

print("Número de acertos: " + str(numero_acertos) + " de " + str(len(linhas)))
print("Taxa de acerto: " + str((numero_acertos) / len(linhas) * 100) + "%")


