import numpy as np
import pandas as pd
from statsmodels.regression.linear_model import  OLS
from statsmodels.tools.tools import add_constant

filename = './ols/ABBNORMAL-2013-3.csv'

datas = pd.read_csv(filename)

datas['XCAC2'] = datas['XCAC'] * datas['XCAC']  

x_cols = ['XCAC2','LNACTF','LEV','ROA']
y_cols = ['ABBFR']
 
# Non lineaire regression

 
x_values = add_constant(datas[x_cols],prepend=False) 
y_values = datas[y_cols]

res1 = OLS(y_values,x_values).fit()

print 'Regression non lineaire : AWCA = b_1*XCAC*XCAC+...'
print(res1.summary()) 

