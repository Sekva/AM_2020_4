# Como só existem duas classes, A e B, vou usar true = A e false = B pra não usar strings
dados_treino = [
      (0, 0),
      (2, 2),
      (4, 4),
      (6, 6),
      (8, 6),
      (10, 4),
      (12, 2),
      (2, 0),
      (3, 1),
      (5, 4),
      (7, 6),
      (8, 3),
      (10, 1),
      (12, 0),
]

resultados_treino = [
      True,
      True,
      True,
      True,
      True,
      True,
      True,
      False,
      False,
      False,
      False,
      False,
      False,
      False,
]

dados_teste = [
      (1, 2),
      (3, 4),
      (5, 6),
      (7, 7),
      (9, 6),
      (11, 4),
      (2, 1),
      (4, 2),
      (6, 4),
      (9, 4),
      (11, 2),
]

resultados_teste = [
      True,
      True,
      True,
      True,
      True,
      True,
      False,
      False,
      False,
      False,
      False,
]

# Vou usar um array de lambdas, cada lambda desse array é um regra
regras = [
        lambda xx : xx[0] >= xx[1], # Se x1 >= x2, então é um voto para a classe A, senão B
        lambda xx : (xx[0] - xx[1]) % 2 == 0 and xx[0] % 2 == 0 and xx[1] % 2 == 0, # Se a diferença entre x1 e x2 for par e os dois forem pares, mais um voto para a classe A, senão B
        lambda xx : xx[0] == 0, # Se x1 é zero, mais um voto para a classe A, senão B
        lambda xx : xx[0] == 0 and xx[1] == 0, # Se os dois dados são zero, então A, senão B
        lambda xx : not (xx[1] == 0), # Se x2 é zero, um voto para a classe B
]

# dados_que_vao_ser_usados = dados_treino
# resultados_que_vao_ser_usados = resultados_treino

dados_que_vao_ser_usados = dados_teste
resultados_que_vao_ser_usados = resultados_teste

# Lista de resultados
# cada entrada dessa lista é um array
# cada array é o resultado do dado aplicado em todas as regras,
# ou seja, lista[3][4] é a classificação do dado dados_treino[3] pela regra regras[4]


lista = list(map( (lambda dado : list(map( (lambda regra : regra(dado)) , regras))) , dados_que_vao_ser_usados))
print("\nResultados:")
print(lista)

# Pra cada resultado, decide o valor pela maioria.
# Por exemplo, se a maioria for A, então o resultado é A
votos_apenas_pra_A = list(map(lambda resultado : list(filter(lambda entrada: entrada, resultado)), lista))

# Tendo o número de votos pra A, e sabendo a quantidade de eleitores (regras), dá pra saber se o resultado é da classe A ou B
resultado_da_votacao = list(map(lambda votos_A : len(votos_A) > (len(regras) / 2), votos_apenas_pra_A))

print("\nResultados finais:")
print(resultado_da_votacao)

from functools import reduce
numero_de_acertos = reduce(lambda a, b : a + b, list(map(lambda r : 1 if r[0] == r[1] else 0, zip(resultado_da_votacao, resultados_que_vao_ser_usados))))
porcentagem = (numero_de_acertos / len(dados_que_vao_ser_usados)) * 100
print("\nNumero de acertos: " + str(numero_de_acertos))
print("\nTaxa de de acertos: " + str(porcentagem) + "%")
print("\nTotal de dados: " + str(len(dados_que_vao_ser_usados)))
