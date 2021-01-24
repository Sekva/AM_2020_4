import pandas
import random
import keras.models
import keras.optimizers 
from sklearn.model_selection import train_test_split
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder
from keras.layers.core import Dense

csv = pandas.read_csv("wine.data", delimiter=",", header=None)
base_dados = csv.to_numpy()

xs = base_dados[:, 1:3]
ys = base_dados[:, 0]
encoder = LabelEncoder()
encoder.fit(ys)
ys = np_utils.to_categorical(encoder.transform(ys))



def ratt(x):
    #x = [camada1, camada2, eta, epocas, holdouts]
    accs = []
    for i in range(x[4]):
        xs_treino, xs_teste, ys_treino, ys_teste = train_test_split(xs, ys, train_size=0.5)

        rede = keras.models.Sequential()

        rede.add(Dense(x[0], input_dim=2, activation="relu"))
        rede.add(Dense(x[1], activation="relu"))
        rede.add(Dense(3, activation="softmax"))

        opt = keras.optimizers.Adam(learning_rate=x[2])
        rede.compile(optimizer=opt, loss="categorical_crossentropy", metrics=["accuracy"])
    
        rede.fit(xs_treino,ys_treino, epochs=int(x[3]))
        loss, accuracy = rede.evaluate(xs_teste, ys_teste)
        #print("Accuracy = {:.2f}".format(accuracy))
        accs.append(accuracy)

    return accs
   

#30 vezes: [0.7528089880943298, 0.6404494643211365, 0.5280898809432983, 0.49438202381134033, 0.43820226192474365, 0.7191011309623718, 0.584269642829895, 0.550561785697937, 0.5730336904525757, 0.584269642829895, 0.617977499961853, 0.5056179761886597, 0.584269642829895, 0.43820226192474365, 0.43820226192474365, 0.5056179761886597, 0.5730336904525757, 0.7191011309623718, 0.6404494643211365, 0.7640449404716492, 0.617977499961853, 0.4606741666793823, 0.6853932738304138, 0.6741573214530945, 0.5730336904525757, 0.6853932738304138, 0.7078651785850525, 0.47191011905670166, 0.617977499961853, 0.7977527976036072]
#acuracias = ratt([1+9, 1+8, 0.001, 9000, 30])

#Media = 0.8146067261695862
#DP = 0.007945018119091611
#acuracias = ratt([1+9, 1+8, 0.001, 9000, 2])

#Media = 0.7808988690376282
#DP = 0.07150516307182452
#acuracias = ratt([12, 6, 0.001, 9000, 2])

#Media = 0.7977527976036072
#DP = 0.015890036238183223
#acuracias = ratt([20, 18, 0.01, 900, 2])




acuracias = ratt([2, 6, 0.1, 1900, 2])


import statistics
media = sum(acuracias) / len(acuracias)
dp = statistics.stdev(acuracias)

print("Media = " +str(media))
print("DP = " +str(dp))


#0.7415730357170105
#0.06
#asd = []
#eta = 0.06
#for ad in range(1):
#    print(ad)
#    accs = []
#    for i in range(6):
#        xs_treino, xs_teste, ys_treino, ys_teste = train_test_split(xs, ys, train_size=0.5, random_state=random.randint(1, 101))
#
#        rede = keras.models.Sequential()
#
#        rede.add(Dense(350, input_dim=2, activation="relu"))
#        rede.add(Dense(50, activation="relu"))
#        rede.add(Dense(3, activation="softmax"))
#
#        opt = keras.optimizers.SGD(learning_rate=eta)
#        rede.compile(optimizer=opt, loss="categorical_crossentropy", metrics=["accuracy"])
#    
#        rede.fit(xs_treino,ys_treino, epochs=400)
#        loss, accuracy = rede.evaluate(xs_teste, ys_teste)
#        accs.append(accuracy)
#        #print("Accuracy = {:.2f}".format(accuracy))
#
#        asd.append(sum(accs) / len(accs))
#    break
#    eta += 0.01
#                   

#print(asd)
#
#maxx = 0
#for a in asd:
#    if maxx < a:
#        maxx = a
#
#print(maxx)
#print("media das medias")
#print(sum(asd) / len(asd))
