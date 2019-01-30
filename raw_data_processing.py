import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os, shutil

# script takes about 6 minutes in total to run

start = 1974 # beginning of record
stop = 2017 # end of record

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

dist_list = open("dist_names.txt").read().splitlines() # read in irrigation
# districts as a list - alphabetical order

################################################################################

# begin process 1 - parse all data by irrigation districts

print('------------------------ process 1 ------------------------')

# the following section of code consolidates data from CSVs of all data from all
# locations for each year into CSVs of all data from each irrigation district
# for each year, and creates directories for each irrigation district and each
# year within each irrigation district 

# time ~ 6 minutes

dir1 = 'Irrigation District Data' # name of first data processing directory

if dir1 in os.listdir(dir_path):
	# quit()
	shutil.rmtree(dir1) # only turn on if need to do
	# again

os.mkdir(dir1) # make directory

for file_ in dist_list: # loop over irrigation districts

	print(file_)

	comtrs = pd.read_csv(dir_path + '/irrigation_districts_with_comtrs/'  +
		file_ + '.csv', index_col=0) # get locations in irrigation district

	os.chdir(dir_path + '/' + dir1) # switch from main directory into dir1

	os.mkdir(file_) # make directory for irrigation district

	os.chdir(dir_path + '/' + dir1 + '/' + file_) # switch into directory for
	# irrigation district

	for i in np.arange(start,stop): # loop over years 1974-2016 for this
	# irrigation district

		path = dir_path + '/raw_data/all_data_normalized_year'+str(i)[2:]+'_by_COMTRS.csv' # path of CSV with all of the data from a given year

		filename = '%d ' %i + file_ # name of CSV: 'year ' + 'irrigation dist'

		df = pd.read_csv(path,index_col=0,sep='\t') # read in all data CSV

		df.loc[comtrs.index].to_csv(filename,index=True) # write data in df 
		# from irrigation district to a new CSV by using location index from
		# the district

# end process 1

os.chdir(dir_path)

################################################################################

# begin process 2 - sum irrigation district crop acreage totals by year

print('------------------------ process 2 ------------------------')

# the following section of code sums data of crop acreage at all locations in a
# given irrigation district for a given crop type ID, and outputs a summary CSV
# of the total for each crop in the irrigation district in a given year

# time ~ 20 seconds

dir2 = 'Irrigation District Summary Data' # name of second data processing
# directory

if dir2 in os.listdir(dir_path):
	# quit()
	shutil.rmtree(dir2) # only turn on if need to do
	# again

os.mkdir(dir2) # make directory

for file_ in dist_list: # loop over irrigation districts

	print(file_)

	os.chdir(dir_path + '/' + dir2) # switch from main directory into dir2

	os.mkdir(file_) # make directory for irrigation district

	os.chdir(dir_path + '/' + dir2 + '/' + file_) # switch into directory for
	# irrigation district

	for i in np.arange(start,stop): # loop over years 1974-2016 for this
	# irrigation district

		path = dir_path+'/'+dir1+'/'+file_+'/'+'/%d ' %i + file_ # path of
		# CSV with irrigation district data from a given year

		filename = '%d ' %i + file_ # name of CSV: 'year ' + 'irrigation dist'

		df = pd.read_csv(path,index_col=0,header=0) # read in irrigation
		# district data CSV

		df.sum(axis=0).to_csv(filename) # sum data for all locations for each
		# crop type ID

# end process 2
 
os.chdir(dir_path)

################################################################################

# begin process 3 - construct step 1 time series

print('------------------------ process 3 ------------------------')

# the following section concatenates the up-till-now-kept-yearly data into time
# series. since there are two sets of crop type codes, one that applies over the
# time interval 1974-1989 and another that applies over the time interval
# 1990-2016, two CSVs for each irrigation district are created. these will be
# concatenated together in the next step, this intermediate step is the last
# unaltered data product. assumptions have to be made about crop type code
# equivalencies in the next step.

# time ~ 10 seconds

dir3 = 'Irrigation District Time Series' # name of third data processing
# directory

if dir3 in os.listdir(dir_path):
	# quit()
	shutil.rmtree(dir3) # only turn on if need to do
	# again

os.mkdir(dir3) # make directory

code74 = pd.read_csv(dir_path+'/codes_1974.csv',index_col=0,header=None) # load
# crop type ID codes that apply from 1974-1989
code90 = pd.read_csv(dir_path+'/codes_1990.csv',index_col=0,header=None) # load
# crop type ID codes that apply from 1990-2016

colum = np.arange(start,stop,1,dtype=int) # creates column header years

for file_ in dist_list: # loop over irrigation districts

	print(file_)

	df1 = pd.DataFrame(0,index=code74.values.astype(str).T
		[0],columns=colum.astype(str)[:16]) # initialize dataframe to load
	# summary CSVs into from years 1974-1989
	df2 = pd.DataFrame(0,index=code90.values.astype(str).T
		[0],columns=colum.astype(str)[16:]) # initialize dataframe to load
	# summary CSVs into from years 1990-2016

	for i in np.arange(start,stop): # loop over years 1974-2016 for this
	# irrigation district

		path = dir_path+'/'+dir2+'/'+file_+'/'+'/%d ' %i + file_ # path of
		# CSV with irrigation district summary data from a given year

		roast = pd.read_csv(path,index_col=0,header=None) # loads summary data

		rindex = np.array(roast.index,dtype=int).astype(str) # loads index

		rindex = rindex[(rindex.astype(int)<=99999) & (rindex.astype(int)>=0)] #
		# cleans index to be inbound values

		if i < 1990:
			df1.loc[rindex,[str(i)]] = roast.loc[rindex.astype
			(int)].values.astype(int) # loads 1974-1989 data into df1
		else:
			df2.loc[rindex,[str(i)]] = roast.loc[rindex.astype
			(int)].values.astype(int) # loads 1990-2016 data into df2

	name1 = '1974-1989 ' + file_ # name df1 file output
	name2 = '1990-2016 ' + file_ # name df2 file output

	os.mkdir(dir_path + '/' + dir3 + '/' + file_) # make irrigation district
	# folder underneath dir3 directory
	os.chdir(dir_path + '/' + dir3 + '/' + file_) # change into irrigation
	# district folder underneath dir3 directory
	df1.to_csv(name1) # write 1974-1989 time series data to CSV
	df2.to_csv(name2) # write 1990-2016 time series data to CSV

# end process 3

os.chdir(dir_path)

################################################################################

# begin process 4 - construct whole period 1974-2016 time series

print('------------------------ process 4 ------------------------')

# the following section concatenates two time series data sets, running from
# 1974-1989 and 1990-2016, respectively, together. this requires the use of a
# library of code equivalencies, which had to be constructed by inspection.

# time ~ 20 seconds

dir4 = 'Irrigation District Data - Final' # name of fourth data processing
# directory

if dir4 in os.listdir(dir_path):
	# quit()
	shutil.rmtree(dir4) # only turn on if need to do
	# again

os.mkdir(dir4) # make directory

match = pd.read_csv(dir_path + 
	'/code_equiv.csv',index_col=0,header=0).fillna(0).astype(int) # loads the
# CSV that equates 1974-1989 codes to 1990-2016 codes. note that code
# equivalencies are not always one-to-one, hence the conditional statements in
# the loop below

active = list(match.index[match['code1'].values != 0]) # creates index of
# current codes used for final df3.to_csv command

m2 = match.set_index(['site_code_1990_2016']) # forgot why this is here

for file_ in dist_list: # loop over irrigation districts

	print(file_)

	path1 = dir_path + '/' + dir3 + '/' + file_ + '/1974-1989 ' + file_ # path
	# to 1974-1989 time series data
	path2 = dir_path + '/' + dir3 + '/' + file_ + '/1990-2016 ' + file_ # path
	# to 1990-2016 time series data

	df1 = pd.read_csv(path1,index_col=0,header=0) # loads 1974-1989 data

	df2 = pd.read_csv(path2,index_col=0,header=0) # loads 1990-2016 data

	new_yrs = list(map(str,np.arange(start,stop))) # string list of 1974-2016

	df3 = pd.DataFrame(columns=new_yrs) # create empty df3 w/ 1974-2016 columns

	count = 0 # initialize count once per irrigation district

	for index, row in m2.iterrows():

		# below here is reading code_equiv and setting the older set to the
		# equivalent newer set. kind of messy but it works.

		if row.values[0] != 0:
			df2.loc[row.values[0]] += df2.loc[index]
		if row.values[2] != 0:
			df1.loc[row.values[1]] += df1.loc[row.values[2]]
		if row.values[3] != 0:
			df1.loc[row.values[1]] += df1.loc[row.values[3]]
		if row.values[4] != 0:
			df1.loc[row.values[1]] += df1.loc[row.values[4]]
		if row.values[5] != 0:
			df1.loc[row.values[1]] += df1.loc[row.values[5]]
		if row.values[1] != 0:
			df3.loc[match.index[count]] = np.append(
				[df1.loc[row.values[1]].values],[df2.loc[index].values])

		count += 1 # increment count

	path3 = dir_path + '/' + dir4 + '/' + file_

	df3 = df3.loc[active] # pare df3 down to current crop codes
	df3.to_csv(path3) # write irrigation district time series to CSV

# end process 4

os.chdir(dir_path)

print('------------------------ end script ------------------------')

# end script