#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 14:54:33 2017

@author: giangblackk
"""

from osgeo import ogr

highwayFileName = './roaddata/R_VN_NHW_Inventory.shp'

dataSource = ogr.Open(highwayFileName)
layer = dataSource.GetLayer(0)
spatialRef = layer.GetSpatialRef()
featureCount = layer.GetFeatureCount()

outputFileName = './R_VN_NHW_Inventory_intersect_nodes.shp'
outDriver = ogr.GetDriverByName('ESRI Shapefile')
outDataSource = outDriver.CreateDataSource(outputFileName)

outLayer = outDataSource.CreateLayer('highway', spatialRef, ogr.wkbPoint)
featureDefn = outLayer.GetLayerDefn()

nodeList = []
for i in range(featureCount):
    feature = layer.GetFeature(i)
    geometry = feature.geometry()
    pointList = geometry.GetPoints()
    pointCount = geometry.GetPointCount()
    firstPoint = (pointList[0][0],pointList[0][1])
    lastPoint = (pointList[-1][0],pointList[-1][1])
    firstPointGeo = ogr.Geometry(ogr.wkbPoint)
    lastPointGeo = ogr.Geometry(ogr.wkbPoint)
    firstPointGeo.AddPoint(firstPoint[0],firstPoint[1])
    lastPointGeo.AddPoint(lastPoint[0],lastPoint[1])
    if firstPoint not in nodeList:
        nodeList.append(firstPoint)
        outFeature = ogr.Feature(featureDefn)
        outFeature.SetGeometry(firstPointGeo)
        outLayer.CreateFeature(outFeature)
    if lastPoint not in nodeList:
        nodeList.append(lastPoint)
        outFeature = ogr.Feature(featureDefn)
        outFeature.SetGeometry(lastPointGeo)
        outLayer.CreateFeature(outFeature)

print(len(nodeList))
outLayer = None
outDataSource = None
layer = None
dataSource = None