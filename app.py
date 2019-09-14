from flask import Flask, render_template, request, redirect

#Modified for Day4 jtharris85 ownership

app = Flask(__name__)

def stockplot():


    import numpy as np

    from bokeh.plotting import figure, output_file, show
    from bokeh.sampledata.stocks import AAPL

# prepare some data
    aapl = np.array(AAPL['adj_close'])
    aapl_dates = np.array(AAPL['date'], dtype=np.datetime64)

    window_size = 30
    window = np.ones(window_size)/float(window_size)
    aapl_avg = np.convolve(aapl, window, 'same')

# output to static HTML file
    output_file("stocks.html", title="stocks.py example")

# create a new plot with a datetime axis type
    p = figure(plot_width=800, plot_height=350, x_axis_type="datetime")

# add renderers
    p.circle(aapl_dates, aapl, size=4, color='darkgrey', alpha=0.2, legend='close')
    p.line(aapl_dates, aapl_avg, color='navy', legend='avg')

# NEW: customize by setting attributes
    p.title.text = "AAPL One-Month Average"
    p.legend.location = "top_left"
    p.grid.grid_line_alpha = 0
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    p.ygrid.band_fill_color = "olive"
    p.ygrid.band_fill_alpha = 0.1

# show the results
    return (p)
stockplot()

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/stocks')
def stocks():
    return render_template('bokeh_plot.html')

if __name__ == '__main__':
  app.run(port=33507,debug=True)
