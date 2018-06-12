from flask import Flask, render_template, request, redirect
import os
import requests
import datetime as dt
import pandas as pd
import io
from bokeh.plotting import figure, show
from bokeh.models import HoverTool
from bokeh.embed import components

app = Flask(__name__)
api_key = os.environ.get('ALPHADVANTAGE_API_KEY')

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/plot')
def drawPlot():
  ticker = request.args.get('ticker')
  if ticker == None:
    ticker = 'AMZN'
  url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&outputsize=compact&datatype=csv&apikey=' + api_key
  r = requests.get(url)
  df = pd.read_csv(io.StringIO(r.text))
  df['timestamp'] = pd.to_datetime(df['timestamp'])
  now = dt.datetime.now()
  startdate = now - dt.timedelta(days=30)
  df = df[df['timestamp'] >= startdate]

  p = figure(title=ticker + ' closing prices from ' + startdate.strftime('%B %d, %Y') + ' to ' + now.strftime('%B %d, %Y'), x_axis_type='datetime')
  p.title.text_font_size = '14pt'
  p.background_fill_color = "beige"
  p.background_fill_alpha = 0.5
  p.xaxis.axis_label = 'Date'
  p.yaxis.axis_label = 'Closing Price ($)'
  p.xaxis.major_label_text_font_size = '12pt'
  p.yaxis.major_label_text_font_size = '12pt'
  p.xaxis.axis_label_text_font_size = '14pt'
  p.yaxis.axis_label_text_font_size = '14pt'
  p.xaxis.axis_label_text_font_style = 'bold'
  p.yaxis.axis_label_text_font_style = 'bold'
  li = p.line(df['timestamp'],df['close'],line_width=4,line_color ='green')
  p.add_tools(HoverTool(tooltips=[('Closing:', '@y{mantissa=6}')], renderers=[li], ))
  script, div = components(p)

  value = None
  value = request.args.get('volumecheckbox')
  if value != None:
    p2 = figure(title=ticker + ' trading volume from ' + startdate.strftime('%B %d, %Y') + ' to ' + now.strftime('%B %d, %Y'), x_axis_type='datetime')
    p2.title.text_font_size = '14pt'
    p2.background_fill_color = "beige"
    p2.background_fill_alpha = 0.5
    p2.xaxis.axis_label = 'Date'
    p2.yaxis.axis_label = 'Trading Volume (1000s)'
    p2.xaxis.major_label_text_font_size = '12pt'
    p2.yaxis.major_label_text_font_size = '12pt'
    p2.xaxis.axis_label_text_font_size = '14pt'
    p2.yaxis.axis_label_text_font_size = '14pt'
    p2.xaxis.axis_label_text_font_style = 'bold'
    p2.yaxis.axis_label_text_font_style = 'bold'
    
    p2.vbar(x=df['timestamp'],top=df['volume']//1000,width=0.5,color='green')
    p2.xgrid.grid_line_color = None
    p2.y_range.start = 0
    script2, div2 = components(p2)

    return render_template('index.html',script=script, div=div, script2=script2, div2=div2)
  else:
    return render_template('index.html',script=script, div=div)


@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(port=33507)
