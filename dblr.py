import json
import numpy as np
from flask import Flask, request
import flask_restful as restful
from sklearn import linear_model

app = Flask(__name__)
api = restful.Api(app)

class lr(restful.Resource):
    def put(self, sn):
        ## get data
        data_raw = request.form['data']
        data_json = json.loads(data_raw)
        data = np.array( [[ float(x), data_json[x]] for x in data_json ])

        ## prepare data
        for i in range(1, len(data)):
            data[i, 0] = np.sum(data[i, 0] + data[i - 1, 0])
        print(data)

        ## fit data
        clf = linear_model.LinearRegression()
        clf.fit(data[:, 0].reshape(-1, 1), data[:, 1])

        ## get coef
        print(clf.coef_[0])
        print(type(clf.coef_[0]))

        ## return
        return({'coef': clf.coef_[0], 'intercept': clf.intercept_})

api.add_resource(lr, '/<string:sn>')

if __name__ == '__main__':
    app.run(debug=True)
