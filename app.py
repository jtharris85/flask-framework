from flask import Flask, render_template, request, redirect

#Modified for Day4 jtharris85 ownership

app = Flask(__name__)

import simplejson as json
import requests
import pandas as pd

#Quandl stocks api
url='https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?api_key=y_KmmxPPeu75fEHcbEg2'

#Print check to determine if it works
def jprint(obj):
    text=json.dumps(obj,sort_keys=True,indent=4)
    print(text)

#Define parameters for filtering. Need to make them selectable!
parameter={'qopts.columns':"ticker,date,open,adj_open,close,adj_close","ticker":"GOOG"}
r=requests.get(url,params=parameter)

#Drop the excess framework
data=json.dumps(r.json()['datatable'])
#Convert back to dictionary and edit columns
data2=json.loads(data)
data2['columns']=['Ticker','Date','Open','Adj Open','Close','Adj Close']
#Convert to string
prep=json.dumps(data2)
#Create dataframe
df=pd.read_json(prep,orient='split')

def stockplot():

    import numpy as np

    from bokeh.plotting import figure, output_file, show

# prepare some data
    stocks = df['Close']
    dates = df['Date']

    window_size = 30
    window = np.ones(window_size)/float(window_size)
    avg = np.convolve(stocks, window, 'same')

# output to static HTML file
    output_file("templates/stocktest.html", title="stock test example")

# create a new plot with a datetime axis type
    p = figure(plot_width=800, plot_height=350, x_axis_type="datetime")

# add renderers
    p.circle(dates, stocks, size=4, color='darkgrey', alpha=0.2, legend='close')
    p.line(dates, stocks, color='navy', legend='avg')

# NEW: customize by setting attributes
    p.title.text = "Stock Open"
    p.legend.location = "top_left"
    p.grid.grid_line_alpha = 0
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    p.ygrid.band_fill_color = "olive"
    p.ygrid.band_fill_alpha = 0.1
    show(p)
stockplot()

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/stocks')
def stocks():
    return render_template('stocktest.html')

if __name__ == '__main__':
  app.run(port=33507,debug=True)
