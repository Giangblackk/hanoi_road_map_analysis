#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 10 16:19:35 2017

@author: giangblackk
"""

#import networkx as nx
#
#G = nx.read_gexf('./highway_line_singlepart_new_123.gexf')
#i=0
#for node in G.nodes_iter():
#    if node in G.neighbors(node):
#        i += 1
#        print(node, G.neighbors(node))
#print(i)

from osgeo import ogr
dataSource = ogr.Open('./highway_line_singlepart.shp')
layer = dataSource.GetLayer()
# layer.SetAttributeFilter("ONEWAY IN ('-1','yes','no')")
spatialRef = layer.GetSpatialRef()

outputFileName = './highway_line_circle_loop.shp'
outDriver = ogr.GetDriverByName('ESRI Shapefile')
outDataSource = outDriver.CreateDataSource(outputFileName)
outLayer = outDataSource.CreateLayer('highway', spatialRef, ogr.wkbLineString)
featureDefn = outLayer.GetLayerDefn()

i = 0
for feature in layer:
    geometry = feature.geometry()
    pointCount = geometry.GetPointCount()
    lastPoint = (geometry.GetPoint(pointCount-1)[0], geometry.GetPoint(pointCount-1)[1])
    firsPoint = (geometry.GetPoint(0)[0],geometry.GetPoint(0)[1])
    middlePointList = []
    for j in range(1,pointCount-1):
        middlePointList.append((geometry.GetPoint(j)[0], geometry.GetPoint(j)[1]))
    if firsPoint in middlePointList or lastPoint in middlePointList:
        i=i+1
        outFeature = ogr.Feature(featureDefn)
        outFeature.SetGeometry(geometry)
        outLayer.CreateFeature(outFeature)
print(i)

outLayer = None
outDataSource = None
layer = None 
dataSource = None