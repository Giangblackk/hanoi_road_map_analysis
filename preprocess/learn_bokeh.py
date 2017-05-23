#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 10:05:03 2017

@author: giangblackk
"""

from bokeh.charts import Histogram, output_file, show
from bokeh.sampledata.autompg import autompg as df
import numpy as np

# df.sort_values(by='cyl', inplace=True)
#hist = Histogram(df, values='hp', color='cyl',
#                 title="HP Distribution by Cylinder Count", legend='top_right')
#
#output_file("histogram_single.html", title="histogram_single.py example")
#
#show(hist)

data = np.array([1,2,3,2,1,2,3,2,3,1,3,3,1,2,1,2])
hist = np.histogram(data, bins=[1,2,3,4])
hist = list(hist)
hist[1] = np.unique(data)
import pandas as pd
dat = pd.DataFrame(np.array(hist).transpose(),columns=['a','b'])
#import plotly.plotly as py
#import plotly.graph_objs as go
#
#data = [go.Bar(
#            x=hist[1],
#            y=hist[0]
#        )]
#
#py.iplot(data, filename='basic-bar')
import seaborn as sns
sns.set_style("whitegrid")
ax = sns.barplot(x="b", y="a", data=dat)
