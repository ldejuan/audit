path = "./csv/"
name = "ALO"
balance = "balanceSheet"
income = "incomeStatement"

filenameb = '{0}{1}:FP_{2}.csv'.format(path,name,balance)
filenamei = '{0}{1}:FP_{2}.csv'.format(path,name,income) 

import pandas as pd
import numpy as np

# read amfblpticker table

amftoblg = 'sbf120tickers.csv'

tamf2blp = pd.read_csv('{0}{1}'.format(path,amftoblg), delimiter = ',') 


def converter(x): 
	try:
		return np.float(x)
	except:
		return 0. 

dict_convert = {'2010' : converter, '2011' : converter, '2012': converter, '2013' : converter, '2014' : converter} 

def getrow(dframe,rname):
	try:
		return dframe.loc[rname]
	except:
		r = pd.DataFrame(np.zeros((1,len(dframe.columns))), columns = dframe.columns,index = [rname])
		
		return r.loc[rname] 
 
def makefinancials(bb_name) :
	filenameb = '{0}{1}:FP_{2}.csv'.format(path,bb_name,balance)

	filenamei = '{0}{1}:FP_{2}.csv'.format(path,bb_name,income) 

	tb = pd.read_csv(filenameb,\
			index_col = 0, \
			delimiter = ';',\
			usecols = [0,1,2,3,4], \
			converters = dict_convert)

	ti = pd.read_csv(filenamei,\
			index_col = 0,\
			delimiter = ';',\
			usecols = [0,1,2,3,4], \
			converters = dict_convert)

	sales = ti.loc['TOTAL REVENUES'] 

	assets = tb.loc['TOTAL ASSETS'] 
	
	incomes = ti.loc['NET INCOME']

	
	wc = tb.loc['TOTAL CURRENT ASSETS'] - tb.loc['TOTAL CASH AND SHORT TERM INVESTMENTS'] -(tb.loc['TOTAL CURRENT LIABILITIES'] - getrow(tb,'Short-Term Borrowings'))

	ewc  = wc.shift()/sales.shift() * sales

	awcacc = (wc - ewc)/ assets.shift() 

	roa = incomes / assets

	margin = incomes / sales

	dmargin = incomes.diff() / sales

	lev = tb.loc['Long-Term Debt']/assets

	r = pd.DataFrame([awcacc, np.log(assets),lev,roa,wc/assets,ewc/assets,margin,dmargin],\
		index = ['ABBFR','LNACTIF','LEV','ROA','BFR','EBFR','MARGE','VMARGE'])

	return r
 
values = ['ABBFR','LNACTIF','LEV','ROA','BFR','EBFR','MARGE','VMARGE']

sbf120raw = {}
years = ['2012','2013']

for year in years :
	
	dfres = pd.DataFrame()

	for item in tamf2blp.iterrows():
		try:
			amfname = item[1]['Name']
			bbname = item[1]['BB_id']
	
			print amfname, bbname 

			dfinancial = makefinancials(bbname.split(':')[0])
	
			df = dfinancial.ix[:,year]

			d = pd.DataFrame(df).T
			d.index = [amfname]

			dfres = dfres.append(d)

		except: 
			print 'Error'
			pass

	dfres.to_csv('./csv/SBF120RESULTATS%s.csv'%year)
	sbf120raw[year] = dfres	
