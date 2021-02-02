import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

from matplotlib import style
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Activation, Bidirectional
from sklearn.model_selection import train_test_split


data = pd.read_csv(sys.argv[1])

X = data[['dailyCloses', 'RSI', 'MACD', 'Stochastic', 'ATR']]
Y = data[['Target']]

numEpochs = 1000
trainTimeSteps = 200
predictTimeSteps = 100
numSamples, numFeatures = X.shape

X = X.as_matrix()
Y = Y.as_matrix()
X = np.array([X[i:i+trainTimeSteps] for i in range(len(X)-trainTimeSteps*2+1)])
Y = np.array([Y[i:i+predictTimeSteps,0] for i in range(trainTimeSteps, len(Y)-trainTimeSteps+1)])


trainX, testX, trainY, testY = train_test_split(X, Y, test_size=int(trainTimeSteps), shuffle=False)

model = Sequential()
model.add(LSTM(5, input_shape=trainX.shape[1:]))
model.add(Dense(5)) 
model.add(Dense(predictTimeSteps))

model.compile(loss='logcosh', optimizer='adam')


performance = model.fit(trainX, trainY, epochs=numEpochs, batch_size=1)
model.save('1000E_200TsT_100TsP.h5')

#plt.figure()
#plt.plot(performance.history['loss'])
#plt.title('Loss over epochs')
#plt.show()


testX = testX[0].reshape(1, trainTimeSteps, numFeatures)
testY = testY[0].reshape(1, predictTimeSteps)

score = model.evaluate(testX, testY, batch_size=1)
#print(score)
prediction = model.predict(testX)[0]

# Let's plot our model's prediction against the test data
plt.figure(figsize=(25, 7))
plt.plot(list(range(len(prediction))), prediction, label='prediction')
plt.plot(list(range(len(testY[0]))), testY[0], label='price')
plt.legend(loc='upper left')
plt.show()