import pandas
import random
import keras.models
import keras.optimizers
from sklearn.model_selection import train_test_split
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder
from keras.layers.core import Dense

import statistics

p1 = False
p2 = True
p3 = False

csv = pandas.read_csv("spiral.csv", delimiter=",", header='infer')
base_dados = csv.to_numpy()

xs = base_dados[:, 0:2]
ys = base_dados[:, 2]
encoder = LabelEncoder()
encoder.fit(ys)
ys = np_utils.to_categorical(encoder.transform(ys))

def ratt(x):
    #x = [n_inp, camada_e_1, camada_e_2, camado_e_3, eta, epocas, holdouts]
    accs = []
    for i in range(x[6]):
        xs_treino, xs_teste, ys_treino, ys_teste = train_test_split(xs, ys, train_size=0.7)
        rede = keras.models.Sequential()

        if x[0] <= 0:
            print("A camada de entrada deve ter algum neuronio")
            exit(0)
                   
        rede.add(Dense(x[0], input_dim=2, activation="sigmoid"))
        if x[1] > 0: rede.add(Dense(x[1], activation="sigmoid"))
        if x[2] > 0: rede.add(Dense(x[2], activation="sigmoid"))
        if x[3] > 0: rede.add(Dense(x[3], activation="sigmoid"))
        rede.add(Dense(3, activation="sigmoid"))
        
        rede.compile(
            optimizer=keras.optimizers.Adam(learning_rate=x[4]),
            loss="categorical_crossentropy",
            metrics=["accuracy"])
        rede.fit(xs_treino, ys_treino, epochs=int(x[5]))
        loss, accuracy = rede.evaluate(xs_teste, ys_teste)
        accs.append(accuracy)

    return accs

if p1:
    casos = [
        [2, 4, 0, 0, 0.3, 500, 2],
        [2, 4, 4, 0, 0.3, 500, 2],
        [2, 4, 4, 4, 0.3, 500, 2],
        [2, 4, 4, 4, 0.3, 1000, 2],
    ]

    resultados = []
    for caso in casos:
        acuracias = ratt(caso)
        media = sum(acuracias) / len(acuracias)
        dp = statistics.stdev(acuracias)
        print("Media = " +str(media))
        print("DP = " +str(dp))
        resultados.append((media, dp))
        for r in resultados: print(r)

    #(0.6255555629730225, 0.10606439926009671)
    #(0.5433333426713943, 0.09985586181814947)
    #(0.373333340883255, 0.0633322465948787)
    #(0.45888889729976656, 0.1461016007719925)

    #(0.8388888835906982, 0.039283728797851976)
    #(0.7888889014720917, 0.10999438162839763)
    #(0.32777778804302216, 0.007856741544885545)
    #(0.3888888955116272, 0.1414213478079398)


    
if p2:
    xs_treino, xs_teste, ys_treino, ys_teste = train_test_split(xs, ys, train_size=0.7)
    rede = keras.models.Sequential()

    rede.add(Dense(2, input_dim=2, activation="sigmoid"))
    rede.add(Dense(4, activation="sigmoid"))
    rede.add(Dense(4, activation="sigmoid"))
    rede.add(Dense(4, activation="sigmoid"))
    rede.add(Dense(3, activation="sigmoid"))
    
    rede.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.3),
        loss="categorical_crossentropy",
        metrics=["accuracy"])

    accs = []
    #for t in range(1000):
    for t in range(20):
        resultado_treinio = rede.fit(xs_treino, ys_treino, epochs=(t*100)+100, validation_split=0.28, initial_epoch=t*100)
        acuracia_validacao = sum(resultado_treinio.history["val_accuracy"]) / len(resultado_treinio.history["val_accuracy"])
        acuracia_treino = sum(resultado_treinio.history["accuracy"]) / len(resultado_treinio.history["accuracy"])
        loss, acuracia_teste = rede.evaluate(xs_teste, ys_teste)

        accs.append((acuracia_treino, acuracia_validacao, acuracia_teste))


    file = open('100k_adam', 'w')
    file.write(str(accs)) 
    file.close()


        
if p3:
    #x = [n_inp, camada_e_1, camada_e_2, camado_e_3, eta, epocas, holdouts]
    casos = [
        [20, 16, 0, 0, 0.3, 500, 10], #98%
        [12, 16, 0, 0, 0.3, 500, 10], #97%
        #[12, 16, 2, 0, 0.3, 500, 2], #32%
        #[12, 16, 32, 0, 0.3, 500, 2],#32%
        #[12, 16, 8, 0, 0.3, 500, 2], #52%
        [9, 5, 0, 0, 0.3, 500, 10]    #94%


        #(0.8355555534362793, 0.29996798227162536)
        #(0.9644444346427917, 0.041507935531112566)
        #(0.973333328962326, 0.014998853981573497)
    ]

    resultados = []
    for caso in casos:
        acuracias = ratt(caso)
        media = sum(acuracias) / len(acuracias)
        dp = statistics.stdev(acuracias)
        print("Media = " +str(media))
        print("DP = " +str(dp))
        resultados.append((media, dp))
        for r in resultados: print(r)
