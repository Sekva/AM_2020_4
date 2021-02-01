arq_lista = open("car.data", "r")
linhas = list(map(lambda linha : linha.replace("\n", ""), arq_lista.readlines()))
linhas = list(map(lambda linha: linha.split(','), linhas))

import random
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)


random.shuffle(linhas)
random.shuffle(linhas)
random.shuffle(linhas)
random.shuffle(linhas)

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


treino_xs = xs[len(linhas)//2:]
treino_ys = ys[len(linhas)//2:]

teste_xs = xs[:len(linhas)//2]
teste_ys = ys[:len(linhas)//2]




from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix

arvores = [2, 4, 16]

for a in arvores:
    arvore = DecisionTreeClassifier(min_samples_leaf=a)
    arvore.fit(treino_xs, treino_ys)
    print("min="+ str(a) + "  -- Acu oracio no treino: " + str(arvore.score(treino_xs, treino_ys)))
    print("min="+ str(a) + "  -- Acu oracio no teste: " + str(arvore.score(teste_xs, teste_ys)))
    print("min="+ str(a) + "  -- Matriz cafusa:\n" + str(confusion_matrix(treino_ys, arvore.predict(teste_xs))))
    print("min="+ str(a) + "  -- Numero de folhas: " + str(arvore.get_n_leaves()))
    print("min="+ str(a) + "  -- Numero de nós (galhos+folhas): " + str(arvore.tree_.node_count))
    print()
    

