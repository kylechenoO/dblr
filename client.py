import requests
import numpy as np
from sklearn import linear_model

## get data and trans to np
url = 'http://127.0.0.1:5000'
json_data = requests.get(url).json()
data = np.array( [[ float(x), json_data[x]] for x in json_data ])
print(data)

## prepare data
for i in range(1, len(data)):
    data[i, 0] = np.sum(data[i, 0] + data[i - 1, 0])
print(data)

## fit data
clf = linear_model.LinearRegression()
clf.fit(data[:, 0].reshape(-1, 1), data[:, 1])

## get coef
print(clf.coef_)
