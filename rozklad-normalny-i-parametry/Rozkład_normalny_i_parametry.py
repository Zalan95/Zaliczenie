import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import math
from typing import List
from scipy.stats import normaltest
import scipy.stats

normalVar = pd.DataFrame(np.random.normal(0,30,100))
normalVar.columns = ['value']
normalVar.head()

sns.distplot(normalVar)
plt.show()

print(normalVar.agg(['mean','median','var','std','kurtosis', 'skew']))

stats, p = normaltest(normalVar)
print(stats, p)
if p > 0.05:
 print ("Rozkład wygląda na normalny")
 
normalVar.to_csv('Wygenerowany_rozklad_normalny.csv')


