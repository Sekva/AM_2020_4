arq_lista = open("car.data", "r")
linhas = list(map(lambda linha : linha.replace("\n", ""), arq_lista.readlines()))
linhas = list(map(lambda linha: linha.split(','), linhas))

import random

random.shuffle(linhas)
random.shuffle(linhas)
random.shuffle(linhas)
random.shuffle(linhas)

from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)

# remove classificação
xs = list(map(lambda e : e[:-1], linhas))
# só as classificações
ys = list(map(lambda e : e[-1], linhas))


from sklearn.preprocessing import LabelEncoder


le = LabelEncoder()
ys = le.fit_transform(ys)


xs2 = []
l2 = LabelEncoder()
for x in xs: xs2.append(l2.fit_transform(x))
xs = xs2



from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier

arvore = DecisionTreeClassifier()
taxas = cross_val_score(arvore, xs, ys, cv=10)
print(taxas)
print(sum(taxas) / len(taxas))

#>>> python q2.py 
#[0.76878613 0.68786127 0.58959538 0.61271676 0.71676301 0.47398844
# 0.70520231 0.50867052 0.65116279 0.45930233]
#0.6174048931307972
#a minha foi bem melhor e bem mais lenta kk
