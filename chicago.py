import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from geopy.distance import geodesic
from datetime import datetime, timedelta
data=pd.read_csv("CTA_-_Ridership_-__L__Station_Entries_-_Daily_Totals.csv")
stations=pd.read_csv("CTA_-_System_Information_-_List_of__L__Stops.csv")
stationid=input('Input station code: ')
imapid=stations.columns.get_loc('MAP_ID')+1
istaname=stations.columns.get_loc('STATION_DESCRIPTIVE_NAME')+1
ilocation=stations.columns.get_loc('Location')+1
def str2geo(locstr):
	return [float(s) for s in locstr[1:len(locstr)-1].split(',')]
for sta in stations.query('MAP_ID == ' + stationid).itertuples(name=None):
	stationname = sta[istaname]
	location = str2geo(sta[ilocation])
	break
closest = [100, 'Dummy Sta', '00000']
for loc in stations.query('MAP_ID != ' + stationid).itertuples(name=None):
	distance = geodesic(location,str2geo(loc[ilocation])).km
	if distance < closest[0]:
		closest[0] = distance
		closest[1] = loc[istaname]
		closest[2] = str(loc[imapid])
print()
print(stationname)
print(location)
print(closest)
print()

date_list = [datetime(2001,1,1) + timedelta(days=i) for i in range(7213)]
everyday = pd.DataFrame(date_list,columns=['date'])
everyday['rides'] = 0
everyday['closestrides'] = 0
print(everyday)

comparedata=data.rename(columns={'rides':'closestrides'}).query('station_id == ' + closest[2])
comparedata["date"]=pd.to_datetime(comparedata["date"])
comparedata=comparedata.sort_values(by="date")

data=data.query('station_id == ' + stationid)
data["date"]=pd.to_datetime(data["date"])
data=data.sort_values(by="date")

done = 0
for index, row in data.iterrows():
	for i in range(done,len(everyday)):
		if everyday['date'][i] == data['date'][index]:
			everyday['rides'][i] = data['rides'][index]
			done = i
			break
done = 0
for index, row in comparedata.iterrows():
	for i in range(done,len(everyday)):
		if everyday['date'][i] == comparedata['date'][index]:
			everyday['closestrides'][i] = comparedata['closestrides'][index]
			done = i
			break
print(everyday)


import matplotlib.pyplot as plt
x=everyday[['closestrides']]
y=everyday['rides']
clf=RandomForestRegressor(n_estimators=50, min_samples_split=2)
clf.fit(x,y)
print(clf.score(x,y))
print(clf.feature_importances_)
p=clf.predict(x)
t=np.arange(0.0,len(everyday))
plt.plot(t,everyday['rides'],'--r')
plt.plot(t,p,'-b')
plt.legend(('real','randomF'))
y=everyday["rides"][0:len(everyday)]
x=np.arange(0,len(everyday))
from scipy.optimize import curve_fit
def func(x,a,b,c,d):
 return a*x*x*x+b*x*x+c*x+d
param=curve_fit(func,x,y)
[a,b,c,d]=param[0]
print(a,b,c,d)
plt.plot(x,func(x,a,b,c,d))
x1=np.arange(0,len(everyday)+360)
plt.plot(x1,func(x1,a,b,c,d))
plt.show()
