from operator import mod
from flask import Flask, request, render_template, session, redirect , Response
import json
import pandas as pd
import pprint


#mongodb connection
# Provide the mongodb atlas url to connect python to mongodb using pymongo

#mongodb functions sample


app = Flask(__name__)
app.debug = True

'''
reading data from src
NOTE : it reads a space after percentage growth so column name is : "Percentage_Growth "
'''
gdpData = pd.read_csv('data/China_GDP_Data.csv')

# @app.route('/')
# def index():
#     first10Records = gdpData.head(10)
#     listOfKeys = gdpData.columns
#     # conversion to ditionary of list -- renders datatable from json
#     allDataJsons = first10Records.to_dict(orient='records')
#     print('-'*50)
#     print('returned first 10 records ... with fields : {}'.format(listOfKeys))
#     print('-'*50,'\n\n\n')
#     pprint.pprint(allDataJsons)
#     # return "<h1>at home {}</h1>".format(first10Records)
#     return render_template('layouts/index.html',
#                            fields=listOfKeys,
#                            data = allDataJsons
#                            )
@app.route('/')
def all_records():
    '''
        return all records
    '''
    allDataJsons = None
    # conversion to ditionary of list -- renders datatable from json
    allDataJsons = gdpData.to_dict(orient='records')


    print("returned {} records".format(len(allDataJsons)))
    return render_template('layouts/allRecords.html',
                           data = allDataJsons
                           )
@app.route('/sample')
def fun1():
    return "<h1> hi! , just a message</h1>"


@app.route('/sample1')
def fun1_2():
    numberOfDocuments = 100
    return "<h1> number of total documents/records in database : {}".format(numberOfDocuments())


@app.route('/sampleChart')
def charts():
    first10Records = gdpData
    # conversion to ditionary of list -- renders datatable from json
    allDataJsons = first10Records.to_dict(orient='records')
    print('rendering charts for years and gdp')
    return render_template('layouts/chartsNew.html',
                           data = allDataJsons
                           )




''' forecasts for per capita gdp '''
forecasts = 'forecast_prediction_using_prophet'
forecastData = pd.read_csv('data/{}.csv'.format(forecasts),index_col=False)
# forecastsData is exported with index -- fix in next version set index to false
# Note it predicts data for 2021-1-1 and 2021-12-31 too
#-- it has two instances of 2021 -- ignore/delete that entry from forecasts csv

# print('columns in forecasts : ',forecastData.columns,'\n\n')
predictions = forecastData.yhat.values
# print(forecastData.head())
# print('predictions : \n\n',predictions)


perCapitaGdp = gdpData.Per_Capita_in_USD.values
yearRanges = [i for i in range(1961,2071)]
# print(yearRanges)
# or just loop over 1..111
# just a modulous example for given range
forecastDataJson = [
    {'Year':yearRanges[i%1961],'Predictions':predictions[i%1961]} for i in range(1961,2071)
]
# print('\n\n predictions in json format: ',forecastDataJson)

@app.route('/sampleChart2')
def chartsPrediction():
    modifiedArray = []
    modifiedArray.extend(perCapitaGdp[::-1])
    for i in range(62,111):
        modifiedArray.append(None)
    
    print('modifiedArray : ',len(modifiedArray))
    print('predictions : ',len(predictions))
    print('yearRanges : ',len(yearRanges))
    
    datesDf = pd.DataFrame({
        'Year':yearRanges , 
        'Per_Capita_in_USD':modifiedArray,
        'Predictions':predictions
        })
    # forecastDataRender = pd.DataFrame({'Year':yearRanges[::-1],'Prediction':forecastData.yhat.values})
    allDataJsons = datesDf.to_dict(orient='records')
    # forecastsJsons = forecastDataRender.to_dict(orient='records')
    print('rendering charts for years and gdp with a prediction line from prophet api')
    return render_template('layouts/chartsNew2.html',
                           data = allDataJsons,
                           predictions = forecastDataJson
                           )





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)