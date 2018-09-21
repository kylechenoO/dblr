import json
import time
import datetime
import numpy as np
from flask import Flask, request
import flask_restful as restful
from sklearn import linear_model
from collections import OrderedDict

app = Flask(__name__)
api = restful.Api(app)

class lr(restful.Resource):
    def put(self, sn):
        ## get data
        data_raw = request.form['data']
        # print(data_raw)

        data_json = json.loads(data_raw, object_pairs_hook=OrderedDict)
        # print(data_json)

        data_dict = OrderedDict()
        base = None
        for key in data_json:
            if base is None:
                base = time.strptime(key, "%Y-%m-%d-%H.%M.%S")
                base = datetime.datetime(base[0], base[1], base[2], base[3], base[4], base[5])
                data_dict['0'] = data_json[key]
                continue
            now = time.strptime(key, "%Y-%m-%d-%H.%M.%S")
            now = datetime.datetime(now[0], now[1], now[2], now[3], now[4], now[5])
            x = ((now - base).seconds / 60) + ((now - base).seconds % 60) * 0.01
            data_dict[x] = data_json[key]

        data = np.array( [[ float(x), data_dict[x] ] for x in data_dict ])
        # print(data)

        ## fit data
        clf = linear_model.LinearRegression()
        clf.fit(data[:, 0].reshape(-1, 1), data[:, 1])

        ## get coef
        # print(clf.coef_[0])
        # print(type(clf.coef_[0]))

        ## return
        return({'coef': clf.coef_[0], 'intercept': clf.intercept_})

api.add_resource(lr, '/<string:sn>')

if __name__ == '__main__':
    app.run(debug=True)
