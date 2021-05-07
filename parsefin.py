path = "./csv/"
name = "ALO"
balance = "balanceSheet"
income = "incomeStatement"

filenameb = '{0}{1}:FP_{2}.csv'.format(path,name,balance)
filenamei = '{0}{1}:FP_{2}.csv'.format(path,name,income) 

import pandas as pd
import numpy as np

# read amfblpticker table

amftoblg = 'cac40tickers.csv'

tamf2blp = pd.read_csv('{0}{1}'.format(path,amftoblg), delimiter = ',') 

def readcac(): 
	
	amfpath = './amf/'
	cacfilename = '{0}CAC40A-2013.csv'.format(amfpath) 

	names = ['SOCIETE',\
		'CAC1',\
		'2013A1',\
		'2012A1',\
		'2013X1',\
		'2012X1',\
		'CAC2',\
		'2013A2',\
		'2012A2',\
		'2013X2',\
		'2012X2']


	tcac = pd.read_csv(cacfilename,\
		header = None, \
		usecols=np.arange(0,11), \
		names = names,\
		index_col = 0)

	return tcac

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

	r = pd.DataFrame([assets,wc/assets,ewc/assets,awcacc,roa,margin,dmargin],\
		index = ['ACTIF','BFR','EBFR','ABBFR','ROA','MARGE','VMARGE'])

	return r
 
tcac = readcac()
companies = tcac.index
values2013 = ['BFR','EBFR','ABBFR','ROA','MARGE','VMARGE', 'CAC1','CAC2','XCAC2013']
values2012 = ['BFR','EBFR','ABBFR','ROA','MARGE','VMARGE', 'CAC1','CAC2','XCAC2012']


tcac['XCAC2013'] = tcac['2013A1']/(tcac['2013A1'] + tcac['2013A2'])
tcac['XCAC2012'] = tcac['2012A1']/(tcac['2012A1'] + tcac['2012A2'])



cac40raw = {}
years = ['2012','2013']

for year in years :
	
	dfres = pd.DataFrame()

	for item in tamf2blp.iterrows():
		try:
			amfname = item[1]['AMF_Name']
			bbname = item[1]['BB_id']
	
			print amfname, bbname 

			dfinancial = makefinancials(bbname.split(':')[0])
	
			df = dfinancial.ix[1:,year]


			df = df.append(tcac.ix[amfname,['CAC1','CAC2','XCAC%s'%year]])
			d = pd.DataFrame(df).T
			d.index = [amfname]

			dfres = dfres.append(d)

		except: 
			print 'Error'
			pass

	dfres.to_csv('./csv/CAC40RESULTATS%s.csv'%year)
	cac40raw[year] = dfres	
