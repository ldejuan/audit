import numpy as np
import pandas as pd
from statsmodels.regression.linear_model import  OLS
from statsmodels.tools.tools import add_constant

filename = './ols/ABBNORMAL-2013-3.csv'

datas = pd.read_csv(filename) 

x_cols = ['XCAC','LNACTF','LEV','ROA','BIG5-BIG5']
y_cols = ['ABBFR'] 
# test absolute value of accruals# 
x_values = add_constant(datas[x_cols],prepend=False) 
y_values = np.abs(datas[y_cols])

res1 = OLS(y_values,x_values).fit()

print 'ABSOLUTE ABBNR'
print(res1.summary()) 

# test absolute value and income increasing #

datas_pos = datas[datas['VMARGE']>0]
x_values = add_constant(datas_pos[x_cols],prepend=False) 
y_values = np.abs(datas_pos[y_cols])

res2 = OLS(y_values,x_values).fit()

print 'ABSOLUTE ABBNR INCOME INCREASING'
print(res2.summary()) 

# test absolute value and income decreasing #

datas_pos = datas[datas['VMARGE']<0]
x_values = add_constant(datas_pos[x_cols],prepend=False) 
y_values = np.abs(datas_pos[y_cols])

res2 = OLS(y_values,x_values).fit()

print 'ABSOLUTE ABBNR INCOME DECREASING'
print(res2.summary()) 
