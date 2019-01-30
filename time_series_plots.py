# this script reads in time series data, sorts the rows by contribution, plots a
# number of them, saves plots for all irrigation districts in a folder

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os, shutil

start = 1974 # beginning of record
stop = 2017 # end of record

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

dist_list = open("dist_names.txt").read().splitlines() # read in irrigation
# districts as a list - alphabetical order

dir5 = 'Time Series Data Plots' # name new directory

if dir5 in os.listdir(dir_path):
	# quit()
	shutil.rmtree(dir5) # only turn on if need to do
	# again

os.mkdir(dir5) # create plots folder for saving plots

os.chdir(dir_path + '/Irrigation District Data - Final') # move into directory
# with time series data in it

n = 4 # number of top crops - keep this small-ish to keep legend clean

for file_ in dist_list: # loop over irrigation districts

	path = dir_path + '/Irrigation District Data - Final/' + file_

	fig = plt.figure(figsize=(15,8))

	df1 = pd.read_csv(path,index_col=0,header=0)
	df1.loc['Total Yearly Acreage Reported'] = df1.sum()
	df1['Total Acreage Reported 1974-2016'] = df1.sum(axis=1)


	df1.sort_values(by='Total Acreage Reported 1974-2016', 
		ascending=False,axis=0,inplace=True)
	print(df1)	
	lab = df1.index[1:n+2]
	labels = [str(lab[i]) for i in np.arange(0,n+1)]

	plt.plot(df1.columns.values[:-1],df1.iloc[0,:-1].values,label='Total Acreage Reported')
	plt.stackplot(df1.columns.values[:-1],df1.iloc[1:n+1,:-1].values,labels=labels)
	plt.xlabel('Year')
	plt.xticks(rotation=90)
	plt.ylabel('Acres')
	plt.title(file_)
	plt.legend()
	fig.savefig(dir_path + '/' + dir5 + '/' + file_ + '.png',bbox_inches='tight') 
	
	# this code can create data files of just the top crops
	# os.chdir(dir_path)
	# df1 = df1.iloc[0:n+1,:-1].T
	# print(df1)
	# df1.to_csv(file_)
	# os.chdir(dir_path + '/Irrigation District Data - Final')










