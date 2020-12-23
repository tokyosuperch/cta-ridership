import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
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
plt.plot(x,y)
plt.plot(x,func(x,a,b,c,d))
x1=np.arange(0,len(data)+360)
plt.plot(x1,func(x1,a,b,c,d))
data["daytype"] = data["daytype"].str.replace("W","0")
data["daytype"] = data["daytype"].str.replace("A","1")
data["daytype"] = data["daytype"].str.replace("U","2")
data["daytype"] = data["daytype"].astype(int)
x=data[['daytype']]
y=data['rides']
clf=RandomForestRegressor(n_estimators=50, min_samples_split=2)
clf.fit(x,y)
print(clf.score(x,y))
print(clf.feature_importances_)
p=clf.predict(x)
t=np.arange(0.0,len(data))
plt.plot(t,data['rides'],'--b')
plt.plot(t,p,'-b')
plt.legend(('real','randomF'))
plt.show()
