import os
import argparse
import seaborn as sns
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt

import pandas as pd

from src import data_path


def read_csv(stock_name):
	with open(data_path(f"{stock_name}.csv"), "r") as csv_file:
		df = pd.read_csv(csv_file)

	return df


def high_low_deviations(df):
	open_vals = df.Open
	close_vals = df.Close
	high = df.High
	low = df.Low
	three_day_open = open_vals.rolling(window=3).mean()
	seven_day_open = open_vals.rolling(window=3).mean()

	compare_vals = seven_day_open

	above_open = (high - compare_vals)/compare_vals
	below_open = (compare_vals - low)/compare_vals

	movement_around_open = pd.concat([above_open, below_open], axis=1).min(axis=1).abs()

	fig, ax = plt.subplots()
	plt.hist(movement_around_open, color='blue', edgecolor='black',
	         bins=100, cumulative=True)
	plt.gca().set(title='Frequency Histogram', ylabel='Frequency')

	ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=len(movement_around_open)))
	plt.show()

	# sns.histplot(open_vals, hist=True, kde=False,
	#              bins=int(180 / 5), color='blue',
	#              hist_kws={'edgecolor': 'black'})


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Basic Stock Analysis')
	parser.add_argument('tag', type=str, help='Which Stock to look at')
	args = parser.parse_args()

	df = read_csv(args.tag)
	high_low_deviations(df)
