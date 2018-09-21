import numpy as np
from flask import Flask
import flask_restful as restful

app = Flask(__name__)
api = restful.Api(app)

class HelloWorld(restful.Resource):
    def get(self):
        data = np.random.randint(0.1, 2, (10, 2))
        data = data + np.random.random(data.shape)
        ret = { x: y for x, y in zip(data[:, 0], data[:, 1])}
        return ret

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
