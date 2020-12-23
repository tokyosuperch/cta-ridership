import pandas as pd
import numpy as np
data=pd.read_csv("CTA_-_Ridership_-__L__Station_Entries_-_Daily_Totals.csv")
data=data.query('station_id == 40850')
data["date"]=pd.to_datetime(data["date"])
data=data.sort_values(by="date")
y=data["rides"][0:len(data)]
x=np.arange(0,len(data))
from scipy.optimize import curve_fit
def func(x,a,b,c,d):
 return a*x*x*x+b*x*x+c*x+d
param=curve_fit(func,x,y)
[a,b,c,d]=param[0]
print(a,b,c,d)
import matplotlib.pyplot as plt
#print("Nov. 3 deaths",int(func(250,a,b,c,d)))
#print("Nov. 23 deaths",int(func(270,a,b,c,d)))
#print("Dec. 23 deaths",int(func(300,a,b,c,d)))
plt.plot(x,y)
plt.plot(x,func(x,a,b,c,d))
x1=np.arange(0,len(data)+360)
plt.plot(x1,func(x1,a,b,c,d))
plt.show()
