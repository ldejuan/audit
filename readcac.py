#!/usr/bin/python
__version__='1.0'
__doc__ = 'read and parse amf joint audit cost'
path = './amf/'
import codecs
import csv
import numpy as np 

def readfile(name='CAC40A-2013.txt'):
	f = codecs.open(path+name,'r',encoding='ascii', errors='ignore')
	data = f.readlines()
	
	f.close()
	
	return data

def parseCAC40(datas, outname = 'CAC40A-2013.csv',istart = 7, iend = 47):
	f = open(path+outname, 'w')
	out =csv.writer(f,delimiter = ';', quoting = csv.QUOTE_ALL) 

	for line in datas[istart:iend]:
		cols = line.split()
		out.writerow(cols) 

	f.close()
		

def doall(name = 'CAC40A-2013',istart = 7, iend = 47):
	datas = readfile('%s.txt'%name)
	parseCAC40(datas,'%s.csv'%name,istart,iend) 

def parseCAC():
	years=[2012,2013]
	sections = ['A','BC']
	params = {'2013A':(7,47),\
		'2012A':(9,53),\
		'2013BC':(2,42),\
		'2012BC':(2,44)}

	for year in years:
		for section in sections:
			try:

				filename = 'CAC40{0}-{1}'.format(section,year)	
				print 'parsing%s'%filename
				istartend = params['{0}{1}'.format(year,section)]
				doall(filename,istartend[0], istartend[1])

			except: 
				print 'Error Parsing %s'%filename
				pass 

def getnparray(name='CAC40A-2013'):
	f = open('{0}{1}.csv'.format(path,name),'r')
	lines = csv.reader(f,delimiter = ';')
	output =[]
	for line in lines: 
		if len(line) >= 11: 
			output.append(line[0:11]) 

 	return np.array(output) 
	
