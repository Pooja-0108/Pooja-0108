#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd


# In[3]:


# students data
student_data = pd.read_csv(r"C:\Users\dell\Downloads\food_coded.csv")


# In[4]:


student_data.head()
student_data.tail()


# In[5]:


to_drop = ['GPA','Gender','breakfast','calories_chicken','calories_day','coffee','comfort_food','comfort_food_reasons','comfort_food_reasons_coded','calories_scone','comfort_food_reasons_coded.1','cuisine','diet_current','diet_current_coded','drink','eating_changes','eating_changes_coded','eating_changes_coded1','father_education','father_profession','fav_cuisine','fav_cuisine_coded','fav_food','soup','thai_food','tortilla_calories','turkey_calories','type_sports','vitamins','waffle_calories','weight','food_childhood','fries','grade_level','greek_food','mother_education','mother_profession','nutritional_check','persian_food','parents_cook','self_perception_weight','healthy_feeling','healthy_meal','ideal_diet','ideal_diet_coded','indian_food','italian_food','life_rewarding','marital_status','meals_dinner_friend']
student_data.drop(to_drop, inplace=True, axis=1)


# In[6]:


student_data.head()


# In[7]:


import matplotlib.pyplot as plt
import pandas as pd 
student_data.replace([np.inf, -np.inf], np.nan, inplace=True)
student_data.replace([np.NaN], 0 , inplace=True)
fig = plt.figure(figsize =(20, 10))
plt.boxplot(student_data)
plt.show()


# In[8]:


print(student_data)


# In[9]:


from sklearn.cluster import KMeans
X = student_data.iloc[:, [7]].values


# In[10]:


Error =[]
for i in range(1, 11):
    kmeans = KMeans(n_clusters = i).fit(X)
    kmeans.fit(X)
    Error.append(kmeans.inertia_)
import matplotlib.pyplot as plt
plt.plot(range(1, 11), Error)
plt.title('Elbow method')
plt.xlabel('No of clusters')
plt.ylabel('Error')
plt.show


# In[11]:


kmeans3 = KMeans(n_clusters=3)
y_kmeans3 = kmeans3.fit_predict(X)
print(y_kmeans3)


# In[12]:


from pandas.io.json import json_normalize
import requests
CLIENT_ID = "W1JUW2EEGBW2Q3DKNFKMM2S3YAJB302VC50IIB2XI3BBPQTB" # your Foursquare ID
CLIENT_SECRET = "3SH3ML5YS1A2JZKHAMKLJOL4XN51ZW4S4AKJRVQG5TXIEQSV" # your Foursquare Secret
VERSION = '20200316'
LIMIT = 10000


# In[13]:


url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
    CLIENT_ID, 
    CLIENT_SECRET, 
    VERSION, 
    13.133521,77.567135,
    30000, 
    LIMIT)


# In[14]:


results = requests.get(url).json()


# In[15]:


results


# In[16]:


venues = results['response']['groups'][0]['items']
nearby_venues = json_normalize(venues)


# In[17]:


nearby_venues


# In[18]:


resta=[]
oth=[]
for lat,long in zip(nearby_venues['venue.location.lat'],nearby_venues['venue.location.lng']):
    url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
      CLIENT_ID, 
      CLIENT_SECRET, 
      VERSION, 
      lat,long,
      1000, 
      100)
    res = requests.get(url).json()
    venue = res['response']['groups'][0]['items']
    nearby_venue = json_normalize(venue)
    df=nearby_venue['venue.categories']

    g=[]
    for i in range(0,df.size):
      g.append(df[i][0]['icon']['prefix'].find('food'))
    co=0
    for i in g:
      if i>1:
        co+=1
    resta.append(co)
    oth.append(len(g)-co)

nearby_venues['restaurant']=resta
nearby_venues['others']=oth


nearby_venues.head()


# In[19]:


nearby_venues.columns


# In[20]:


n = nearby_venues.drop(['referralId', 'reasons.count', 'reasons.items', 'venue.id',
       'venue.name','venue.location.labeledLatLngs', 'venue.location.distance',
       'venue.location.cc', 'venue.location.city', 'venue.location.state',
       'venue.location.country', 'venue.categories', 'venue.photos.count', 'venue.photos.groups',
       'venue.location.address', 'venue.location.crossStreet',
       'venue.location.postalCode', 'venue.location.neighborhood',
       'venue.venuePage.id','venue.location.formattedAddress'],axis = 1)


# In[21]:


n.columns


# In[22]:


n


# In[38]:


n = n.dropna()
n = n.rename(columns = {'venue.location.lat': 'lat' ,'venue.location.lng':'lng','others':'Fruits,Vegetables,Groceries','restaurant':'Restaurants'})
n


# In[24]:


f=['lat','lng']
X = n[f]


# In[25]:


kmeans3 = KMeans(n_clusters=3)
y_kmeans3 = kmeans3.fit_predict(X)
print(y_kmeans3)


# In[32]:


import folium
mapit = None
latlon = [ (13.032086,77.590020), (13.06394,77.591492), (13.011772,77.556788),(12.991578,77.554561),(12.910901,77.551448),(12.875989,77.595602),(12.873000,77.621000),(13.168697,77.632389),(13.368001,77.680911)]
for coord in latlon:
    mapit = folium.Map( location=[ coord[0], coord[1] ] )
tooltip = "Click me!"
folium.Marker(
[13.032086,77.590020], popup="<i>Mt. Hood Meadows</i>", tooltip=tooltip
).add_to(mapit)
tooltip = "Click me!"
folium.Marker(
[13.06394,77.591492], popup="<i>Mt. Hood Meadows</i>", tooltip=tooltip
).add_to(mapit)
tooltip = "Click me!"
folium.Marker(
[13.011772,77.556788], popup="<i>Mt. Hood Meadows</i>", tooltip=tooltip
).add_to(mapit)
tooltip = "Click me!"
folium.Marker(
[12.991578,77.554561], popup="<i>Mt. Hood Meadows</i>", tooltip=tooltip
).add_to(mapit)
folium.Marker(
    location=[12.910901,77.551448],
    popup="Some Other Location",
    icon=folium.Icon(color="red"),
).add_to(mapit)
folium.Marker(
    location=[12.875989,77.595602],
    popup="Some Other Location",
    icon=folium.Icon(color="red"),
).add_to(mapit)
folium.Marker(
    location=[12.873000,77.621000],
    popup="Some Other Location",
    icon=folium.Icon(color="red"),
).add_to(mapit)
folium.Marker(
    location=[12.910901,77.551448],
    popup="Some Other Location",
    icon=folium.Icon(color="green"),
).add_to(mapit)
folium.Marker(
    location=[13.368001,77.680911],
    popup="Some Other Location",
    icon=folium.Icon(color="green"),
).add_to(mapit)


# In[33]:


mapit


# 
