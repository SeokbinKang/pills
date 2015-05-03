#!/usr/bin/python

from flask import Flask, request, render_template
from flask.ext.restful import Resource, Api
import dataprocess
from flask_restful import reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('ageMin', type=int, help='Invalid number')
parser.add_argument('ageMax', type=int, help='Invalid number')
parser.add_argument('gap', type=int, help='Invalid number')
parser.add_argument('overlap', type=int, help='Invalid number')
parser.add_argument('drugList', type=list, help='Invalid list')
parser.add_argument('fileName', type=str, help='Invalid file name')


class Data(Resource):

  def get(self):
    args = parser.parse_args(strict=True)

    ageMin = 0
    if (args['ageMin'] is not None):
      ageMin = args['ageMin']
        
    ageMax = 100
    if (args['ageMax'] is not None):
      ageMin = args['ageMax']

    gap = 0
    if (args['gap'] is not None):
      gap = args['gap']

    overlap = 0
    if (args['overlap'] is not None):
      overlap = args['overlap']

    fileName = 'data/Ace_Beta_Diur_1SamplingRate.txt'
    if (args['fileName'] is not None):
      fileName = args['fileName']


    drugList = ['1', '3', '5']
    if (args['drugList'] is not None):
      drugList = args['drugList']
      drugList = "".join(drugList)

    patients, drugStats = dataprocess.process(fileName = fileName, drugList = drugList, overlap = overlap, gap = gap, ageMin = ageMin, ageMax = ageMax)

    patientsObj = dataprocess.patientsJSON(patients)
    drugsObj = dataprocess.drugsJSON(drugStats, drugList)

    return { "patients": patientsObj,
             "drugs" : drugsObj }
                 

api.add_resource(Data, '/data')

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/example')
def example():
    return render_template('example.html')


if __name__ == '__main__':
    app.run(debug=True)
