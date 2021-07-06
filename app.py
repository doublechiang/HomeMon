#!/usr/bin/env python3
import os
from flask import Flask, request, redirect, render_template, url_for
from bokeh.plotting import figure
from bokeh.embed import json_item
from bokeh.models import ColumnDataSource
import json

import pandas as pd
import database as dblyr
from sqlalchemy.sql import select

from flask import Flask, render_template
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput
from bokeh.io import curdoc
from bokeh.resources import INLINE
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Spectral3


# local import
import temperature

app = Flask(__name__)
app.config['APPLICATION_ROOT'] = 'HomeMon'

@app.route('/', methods=['get', 'post'])
def root():
    conn = dblyr.Database().getConn()
    engine = dblyr.Database().getEngine()

    s = select(temperature.Temperature).where(temperature.Temperature.sensor == '95132,us')
    df = pd.read_sql(s, conn)
    df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %H:%M:%S')
    source = ColumnDataSource(df)

    nest = select(temperature.Temperature).where(temperature.Temperature.sensor == 'nest')
    nest_df = pd.read_sql(nest, conn)
    nest_df['datetime'] = pd.to_datetime(nest_df['datetime'], format='%Y-%m-%d %H:%M:%S')
    nest_source = ColumnDataSource(nest_df)


    fig = figure(plot_height=600, plot_width=720, tooltips=[("Title", "@title"), ("Released", "@released")])
    fig.line(x='datetime', y='temp', source=source, line_width=2, legend='95132,US')
    fig.line(x='datetime', y='temp', source=nest_source, line_width=2, color=Spectral3[2], legend='Nest')
    fig.xaxis.axis_label = "DateTime"
    fig.yaxis.axis_label = "Temperature"

    # source.data = dict(
    #     x = [d['imdbrating'] for d in currMovies],
    #     y = [d['numericrating'] for d in currMovies],
    #     color = ["#FF9900" for d in currMovies],
    #     title = [d['title'] for d in currMovies],
    #     released = [d['released'] for d in currMovies],
    #     imdbvotes = [d['imdbvotes'] for d in currMovies],
    #     genre = [d['genre'] for d in currMovies]
    # )

    script, div = components(fig)
    return render_template(
        'temp.html',
        plot_script=script,
        plot_div=div,
        js_resources=INLINE.render_js(),
        css_resources=INLINE.render_css(),
    ).encode(encoding='UTF-8')



@app.route('/plot')
def plot():
    conn = dblyr.Database().getConn()
    engine = dblyr.Database().getEngine()
    s = select([temperature.Temperature])
    df = pd.read_sql(s, conn)
    source = ColumnDataSource(df)
    p = figure(x_axis_type="datetime", plot_width=400, plot_height=400)
    p.line(x='index', y='temp', source=source, line_width=2)

    # p = make_plot('petal_width', 'petal_length')
    return json.dumps(json_item(p, "myplot"))

    

if __name__ == '__main__':
    app.run(port=5000)
