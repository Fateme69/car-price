import requests
import re
from bs4 import BeautifulSoup
import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import tree
from sklearn.neighbors import NeighborhoodComponentsAnalysis, KNeighborsClassifier,NearestCentroid
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV, StratifiedKFold



final_list = []
element = {}
cnx = mysql.connector.connect(user= 'root',password='A3man_1369',
                              host='127.0.0.1',
                              database= 'car_db')
cursor = cnx.cursor()

#####################################
###fetching data from website and create datebase

# for page in range(100):
#     url = "https://www.truecar.com/used-cars-for-sale/listings/?page="+str(page+1)
#     r = requests.get(url)
#     print(page+1)
#     soup = BeautifulSoup(r.text,'html.parser')
#     names = soup.find_all('span' , attrs={'class':'vehicle-header-make-model text-truncate'})
#     card = soup.find_all('div', attrs={'class' : 'linkable card card-shadow vehicle-card _1qd1muk'})
#     prices = soup.find_all('div', attrs={'data-test':'vehicleCardPricingBlockPrice'})
#     usages = soup.find_all('div' , attrs= {'data-test':'vehicleMileage'})
#     years = soup.find_all('div',attrs={'data-test':'vehicleCardYearMakeModel'})
#     for i in range(len(card)):
#         element['company'] = (re.findall(r'(\w+)\s\w',names[i].text)[0]).lower()
#         element['model'] =(re.findall(r'\w\s(.+)', names[i].text)[0]).lower()
#         element['year'] = int(re.findall(r'.*(20\d{2}|19\d{2}).*',years[i].text)[0])
#         element['price'] = int(prices[i].text[1:].replace(',', ''))
#         element['usage'] = int(usages[i].text[:-6].replace(',',''))
#         final_list.append(element.copy())
#         cursor.execute('INSERT INTO car_tb VALUES (\'%s\',\'%s\',\'%d\',\'%d\',\'%d\')' %
#                        (element['company'],element['model'],element['year'],element['usage'],element['price']))
#
#
# cnx.commit()
####################################

######################################
#####export car_tb table to csv file
# query = 'SELECT * FROM car_tb;'
# cursor.execute(query)
# df = pd.DataFrame(cursor)
# df.to_csv (r'C:\Users\Apple3\Desktop\exported_data.csv', index = False)
#####################################

##################################
#########geting input
new_company = input('please enter the company:').lower()
new_model = input('please enter the model:').lower()
new_year = float(input('pleas enter the year:'))
new_usage = float(input('plaese enter the usage:'))

####################################

####################################
####Reading csv file
car_info = pd.read_csv('exported_data.csv')
X = pd.DataFrame({'year': [],'usage': []})
y = pd.DataFrame({'price': []})
# X = []
# y = []
for i  in range(len(car_info.company)):
    if (car_info.company.values[i]).lower() == new_company:
        if (car_info.model.values[i]).lower() == new_model:
            X = X.append({'year':car_info.year.values[i], 'usage':car_info.usage.values[i]},ignore_index=True)
            y =  y.append({'price':car_info.price.values[i]}, ignore_index=True)
            
####################################

#####################################
#####linear regression process
new_data = pd.DataFrame({'year':[new_year],'usage':[new_usage]})
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3)


clf = NearestCentroid()
clf.fit(X_train, y_train)
print(clf.score(X_test, y_test))
print (int(clf.predict(new_data)))
# a = nca_pipe.predict({'year':2017.0,'usage':201161.0})
cnx.close()
