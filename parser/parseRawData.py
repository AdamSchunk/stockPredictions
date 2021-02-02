import sys
import numpy as np
import pandas as pd

#RSI
#MACD
#ATR
#Stochastic


#you lose the first 14 datapoints from RSI

def parseData(rawFileLocation):
	data = pd.read_csv(rawFileLocation)
	dailyCloses = data["Adj Close"]
	dailyGain = [j-i if j-i > 0 else 0 for i, j in zip(dailyCloses[:-1], dailyCloses[1:])]
	dailyLoss = [(j-i)*-1 if j-i < 0 else 0 for i, j in zip(dailyCloses[:-1], dailyCloses[1:])]
	dailyHigh = data["High"]
	dailyLow = data["Low"]
	
	parsedData = np.array(list(zip(dailyCloses[1:],dailyGain, dailyLoss, dailyHigh, dailyLow)))
	return parsedData
	
	'''
	computes RSI by calculating the daily loss and daily gain averages
	over a period of time. The first n datapoints where n = period are
	ignored in the dataset to build up the correct averages.
	padding is added to the front of the returned set to keep sizes consistent.
	'''
def getRSI(parsedData, period):

	RSI = [np.nan]*period
	dailyGain = parsedData[:,1]
	dailyLoss = parsedData[:,2]
	prevAG = sum(dailyGain[0:period])/period
	prevAL = sum(dailyLoss[0:period])/period
	
	
	for i in range(period, len(parsedData)):
		AG = (prevAG*(period-1) + dailyGain[i])/14
		AL = (prevAL*(period-1) + dailyLoss[i])/14
		prevAG = AG
		prevAL = AL
		RS = AG/AL
		RSI.append(100 - 100/(1+RS))
		
	return np.array(RSI)
	
	
	
def getMACD(dailyCloses, period1 = 12, period2 = 26, signal = 9):
	df = pd.DataFrame({'dailyCloses':dailyCloses})
	EMA1 = pd.DataFrame.ewm(df["dailyCloses"],span=period1).mean()
	EMA2 = pd.DataFrame.ewm(df["dailyCloses"],span=period2).mean()
	MACD = EMA1-EMA2

	Signal = pd.DataFrame.ewm(MACD,signal).mean()
	#print(MACD)
	return MACD - Signal
	
def getStochastic(dailyCloses, period):
	df = pd.DataFrame({'dailyCloses':dailyCloses})
	lows = pd.DataFrame.rolling(df['dailyCloses'], period).min()
	highs = pd.DataFrame.rolling(df['dailyCloses'], period).max()
	res = 100 * (df['dailyCloses'] - lows) / (highs - lows)
	return res

def getATR(dailyCloses, highs, lows, period):
	#h-l
	#h-pc
	#l-pc
	
	df = pd.DataFrame({'dailyCloses':dailyCloses, 'lows':lows, 'highs':highs})
	df['H-L'] = abs(df['highs']-df['lows'])
	df['H-PC'] = abs(df['highs']-df['dailyCloses'].shift(1))
	df['L-PC'] = abs(df['lows']-df['dailyCloses'].shift(1))
	TR = df[['H-L','H-PC','L-PC']]
	
	TR['mean'] = TR.mean(axis=1)
	return TR['mean']
	
if __name__ == "__main__":
	parsedData = parseData(sys.argv[1])
	
	RSIperiod = 14
	stoPeriod = 14
	atrRange = 5
	
	dailyCloses = parsedData[:,0]
	highs = parsedData[:,3]
	lows = parsedData[:,4]
	RSI = getRSI(parsedData, RSIperiod)
	MACD = getMACD(dailyCloses, 12, 26, 9)
	stochastic = getStochastic(dailyCloses, stoPeriod)
	trueRange = getATR(dailyCloses, highs, lows, atrRange)
	
	print(len(dailyCloses))
	print(len(RSI)) #padding until RSIperiod
	print(len(MACD)) #full
	print(len(stochastic)) # nan stoPeriod at front
	print(len(trueRange)) # first entry invalid
	#print(len(target)) #last entry padding
	
	features = pd.DataFrame({'dailyCloses':dailyCloses})
	features['RSI'] = RSI
	features['MACD'] = MACD
	features['Stochastic'] = stochastic
	features['ATR'] = trueRange
	features = (features - features.mean()) / (features.max() - features.min())
	features['Target'] = features['dailyCloses']
	
	features = features.dropna()
	

	print(features)
	
	
	features.to_csv(sys.argv[2], index=False)
	
	