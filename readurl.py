#!/usr/bin/python
__version__='1.0'
__title__='Read financial urls'
Tai__doc__ =' test reading financial urls'
from urllib2 import Request,urlopen
from  urllib import urlencode
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

import xml.dom.minidom as minidom 
from lxml import html,etree
import numpy as np

strbusweek = 'http://investing.businessweek.com/research/stocks/financials/financials.asp?ticker=%s&dataset=balanceSheet&period=A&currency=native'
tickers = ['AC:FP','ADP:FP']
strfinratios = 'http://investing.businessweek.com/research/stocks/financials/ratios.asp?ticker=%s'
strfinurl = 'http://investing.businessweek.com/research/stocks/financials/financials.asp?ticker=%s&dataset=incomeStatement&period=A&currency=native'

busweekurl = 'http://investing.businessweek.com/research/stocks/financials/financials.asp?ticker={0}&dataset={1}&period=A&currency=native'

datasets = ['balanceSheet','incomeStatement'] 

path = './csv/'
def readtickers():
	tickers = np.genfromtxt(path+'sbf120tickers.csv',\
			 dtype=None,\
			 delimiter=',',\
			 skip_header=1)

	return tickers
 
def testread():
	url = strbusweek%tickers[1]
	resq = Request(url)
	response = urlopen(resq)
	result = response.read()
	
	return result

def readfinancial(ticker,dataset='balanceSheet'):
	try:
		url = busweekurl.format(ticker,dataset) 
		doc = html.fromstring(urlopen(Request(url)).read())
		for elt in doc.getiterator('table'):
			try :
				elt.attrib.values().index('financialStatement')
				return elt

			except ValueError: 
				pass
	except ValueError:
		print 'ticker_%s'%ticker
	return 0 
def remove(text):
	try: 

		if text == u'\xa0':
			out = 'None'
		else:
			out =text	
			out =out.replace(',','')
	except : 
		out = 'None'
	return out

def table2csv(htmltable):
	out = ''
	j =0 

	header = htmltable[0]
	header.remove(header.getchildren()[1])

	for col in header:
		try: 
			out = out +'%s;'%col.find('br').tail
		except:
			out = out +'None;'
	out = out +'\n'

 
	tr_iter = htmltable.iter('tr')
	tr_iter.next() 
	for line in tr_iter:
		for col in line.iter('td'):
			out = out + '%s;'%remove(col.text)
		out = out + '\n'
	return out

def csvtofile(csvfile,ticker):
	f = open(ticker,'w')
	f.write(csvfile)
	f.close()
	return 0
 
def retrievesave(ticker): 
	try:
		print 'factoring %s'%ticker
		for dataset in datasets:
			xmltable =readfinancial(ticker,dataset)
			csvtable = table2csv(xmltable)
			csvtofile(csvtable,'{2}_{0}_{1}.csv'.format(ticker,dataset,path)) 
			print 'Success {0}_{1}\n'.format(ticker,dataset) 
 
	except ValueError:
		print '%s not read'%ticker

	except AttributeError:
		print '%s not read'%ticker

	except:
		print '%s not read'%ticker

	return 0
INAME = 0
ITICKER =1 

def retrieveall():
	tickers = readtickers() 
 
	for ticker in tickers:
		retrievesave(ticker[ITICKER]) 
	
	return 0

finratios = {'Total Debt/Equity':0, 'Return on Assets':0, 'EBITDA Margin':0} 

def retrieveratios(ticker):
	try:
		print strfinratios%ticker

		hurl = html.fromstring(urlopen(Request(strfinratios%ticker)).read())
		ratios = {}
		for table in hurl.iter('table'): 
			for p in table.iter('p'):
				print p.text
				if finratios.has_key(p.text):
					print 'found %s'%p.text
					ratios[p.text] = p.getparent().getparent()[1].getchildren()[0].text
		return ratios
	except: 
		print '%s not read'%ticker

if __name__=='__main__': 
	retrieveall()
  	 
def htmltoxml(sthtml):
	doc = html.fromstring(sthtml)
	return etree.tostring(doc) 

def readtotree():
	url = strbusweek%tickers[0]
	resq = Request(url)
	response = urlopen(resq)
	return etree.tostring(response)		
	
class MyHTMLParser(HTMLParser):
	def handle_starttag(self,tag,attrs):
		if tag == 'table': 
			print "Start tag:", tag
			for attr in attrs:
				print "  attr: ", attr
