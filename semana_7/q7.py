arq_lista = open("wine.data", "r")
linhas = list(map(lambda linha : linha.replace("\n", ""), arq_lista.readlines()))
linhas = list(map(lambda linha: linha.split(','), linhas))

rng = 463

xs = list(map(lambda a : a[1:], linhas))
ys = list(map(lambda a : str(a[0]), linhas))


from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
encoded_Y = encoder.fit_transform(ys)
# tem q mandar pra list pq o tipo dinamico de python é incapaz de inferir ndarray -> list
ys = np_utils.to_categorical(encoded_Y).tolist()

print(type(ys))

for idx_x in range(len(xs)):
    xs[idx_x] = list(map(lambda el : float(el), xs[idx_x]))

xs_ntratado = []
for x in xs:
    xs_ntratado.append(x.copy())

attrs = []
for idx_attr in range(len(xs[0])):
    attrs.append(list(map(lambda el : float(el[idx_attr]), xs)))

maxs = list(map(lambda attr : max(attr), attrs))
mins = list(map(lambda attr : min(attr), attrs))

for x in xs:
    for idx, (imax, imin) in enumerate(zip(maxs, mins)):
        x[idx] = (x[idx] - imin) / (imax - imin)

xs_tratado = xs

from sklearn.model_selection import train_test_split
X_train_ntratado, X_test_ntratado, y_train_ntratado, y_test_ntratado = train_test_split(xs_ntratado, ys, test_size=0.3, random_state=rng)
X_train_tratado, X_test_tratado, y_train_tratado, y_test_tratado = train_test_split(xs_tratado, ys, test_size=0.3, random_state=rng)

# tipos_dados[0] é sem tratamento
# tipos_dados[1] é com tratamento
tipos_dados = []

tipos_dados.append((X_train_ntratado, X_test_ntratado, y_train_ntratado, y_test_ntratado))
tipos_dados.append((X_train_tratado, X_test_tratado, y_train_tratado, y_test_tratado))

from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import Adam

accs = []
for X_train, X_test, y_train, y_test in tipos_dados:
    nn = Sequential()
    nn.add(Dense(10, input_dim=13, activation="sigmoid"))
    nn.add(Dense(3, activation="softmax"))
    opt = Adam(learning_rate=0.5)
    nn.compile(optimizer=opt, loss="categorical_crossentropy", metrics=["accuracy"])
    nn.fit(X_train, y_train, epochs=500, verbose=2)
    _, accuracy = nn.evaluate(X_test, y_test, verbose=1)
    accs.append(accuracy)

print(accs)

#acho que deu overfitting nos dados tratados já que chegou em quase 100% no treino


#4/4 - 0s - loss: 0.2697 - accuracy: 0.9274
#2/2 [==============================] - 0s 24ms/step - loss: 0.2405 - accuracy: 0.9444
#[0.29629629850387573, 0.9444444179534912]
 
