from __future__ import print_function

import os
import json
import pickle
import io
import sys
import signal
import traceback

import flask

import pandas as pd

prefix = '/opt/ml/'
model_path = os.path.join(prefix, 'model')

class ScoringService(object):
    model = None               

    @classmethod
    def get_model(cls):
        if cls.model == None:
            with open(os.path.join(model_path, 'decision-tree-model.pkl'), 'rb') as inp:
                cls.model = pickle.load(inp)
        return cls.model

    @classmethod
    def predict(cls, input):

        clf = cls.get_model()
        return clf.predict(input)

app = flask.Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    health = ScoringService.get_model() is not None  

    status = 200 if health else 404
    return flask.Response(response='\n', status=status, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def transformation():
    data = None

    if flask.request.content_type == 'text/csv':
        data = flask.request.data
        s = io.BytesIO(data)
        data = pd.read_csv(s, header=None)
    else:
        return flask.Response(response='This predictor only supports CSV data', status=415, mimetype='text/plain')

    print('Invoked with {} records'.format(data.shape[0]))

    predictions = ScoringService.predict(data)

    out = io.StringIO()
    pd.DataFrame({'results':predictions}).to_csv(out, header=False, index=False)
    result = out.getvalue()

    return flask.Response(response=result, status=200, mimetype='text/csv')
