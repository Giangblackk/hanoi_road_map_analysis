#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 17:32:10 2017

@author: giangblackk
"""

from osgeo import ogr
import networkx as nx
import numpy as np

# read source dataset
highwayFileName = './highway_line_singlepart.shp'
dataSource = ogr.Open(highwayFileName)
layer = dataSource.GetLayer(0)
spatialRef = layer.GetSpatialRef()
featureCount = layer.GetFeatureCount()
print(featureCount)
# layer.SetAttributeFilter("ONEWAY NOT IN ('yes', 'no','-1')")
# layer.SetAttributeFilter("ONEWAY IN ('-1','yes','no')")
# get attribute list
attributeList = []
layerDefinition = layer.GetLayerDefn()
for i in range(layerDefinition.GetFieldCount()):
    fieldName =  layerDefinition.GetFieldDefn(i).GetName()
    attributeList.append(fieldName)
attributeList.remove('TOLL')
attributeList.remove('TRACKTYPE')
attributeList.remove('DISUSED')
# create graph
G = nx.DiGraph()
pointList = []
i = 0
roadList = []
for feature in layer:
    geometry = feature.geometry()
    pointCount = geometry.GetPointCount()
    # first point
    firstPoint = (geometry.GetPoint(pointCount-1)[0], geometry.GetPoint(pointCount-1)[1])
    if not firstPoint in pointList:
        pointList.append(firstPoint)
        G.add_node(i, lng=firstPoint[0], lat=firstPoint[1])
        firstNodeID = i
        i = i + 1
    else:
        # firstNodeID = pointList.index(firstPoint)
        for nodeidx in G.nodes_iter():
            if G.node[nodeidx]['lng'] == firstPoint[0] and G.node[nodeidx]['lat'] == firstPoint[1]:
                firstNodeID = nodeidx
    # last point
    lastPoint = (geometry.GetPoint(0)[0],geometry.GetPoint(0)[1])
    if not lastPoint in pointList:
        pointList.append(lastPoint)
        G.add_node(i, lng=lastPoint[0], lat=lastPoint[1])
        lastNodeID = i
        i = i + 1
    else:
        # lastNodeID = pointList.index(lastPoint)
        for nodeidx in G.nodes_iter():
            if G.node[nodeidx]['lng'] == lastPoint[0] and G.node[nodeidx]['lat'] == lastPoint[1]:
                lastNodeID = nodeidx
###############################################################################
    edges = G.edges()
    for edge in edges:
        headID = edge[0]
        tailID = edge[1]
        middle = G[headID][tailID]['middle']
        if firstPoint in middle:
            attributeDict = G[headID][tailID]
            G.remove_edge(headID, tailID)
            G.add_edge(headID, firstNodeID, attr_dict=attributeDict)
            G.add_edge(firstNodeID, tailID, attr_dict=attributeDict)
        elif lastPoint in middle:
            attributeDict = G[headID][tailID]
            G.remove_edge(headID, tailID)
            G.add_edge(headID, lastNodeID, attr_dict=attributeDict)
            G.add_edge(lastNodeID, tailID, attr_dict=attributeDict)
###############################################################################
    middlePointList = []
    for j in range(1,pointCount-1):
        middlePointList.append((geometry.GetPoint(j)[0], geometry.GetPoint(j)[1]))
    # create link
    if feature.GetField('ONEWAY') == '-1':
        G.add_edge(lastNodeID, firstNodeID)
        for attribute in attributeList:
            G[lastNodeID][firstNodeID][attribute] = feature.GetField(attribute) if feature.GetField(attribute) is not None else ''
        G[lastNodeID][firstNodeID]['middle'] = middlePointList
    elif feature.GetField('ONEWAY') == 'yes':
        G.add_edge(firstNodeID, lastNodeID)
        for attribute in attributeList:
            G[firstNodeID][lastNodeID][attribute] = feature.GetField(attribute) if feature.GetField(attribute) is not None else ''
        G[firstNodeID][lastNodeID]['middle'] = middlePointList
    else:
        G.add_edge(firstNodeID, lastNodeID)
        G.add_edge(lastNodeID, firstNodeID)
        for attribute in attributeList:
            G[firstNodeID][lastNodeID][attribute] = feature.GetField(attribute) if feature.GetField(attribute) is not None else ''
            G[lastNodeID][firstNodeID][attribute] = feature.GetField(attribute) if feature.GetField(attribute) is not None else ''
        G[firstNodeID][lastNodeID]['middle'] = middlePointList
        G[lastNodeID][firstNodeID]['middle'] = middlePointList
# remove middle properties
for edge in G.edges_iter():
    G[edge[0]][edge[1]].pop('middle')
# check if 2 node same lat long
lat = G.node[0]['lat']
lng = G.node[0]['lng']
sameCount = 0
for i in G.nodes_iter():
    if G.node[i]['lat'] == lat and G.node[i]['lng'] == lng:
#        print('same')
        sameCount += 1
    else:
        lat = G.node[i]['lat']
        lng = G.node[i]['lng']
print(sameCount)
# nx.write_gexf(G,'./highway_line_singlepart.gexf')
nx.write_gexf(G,'./highway_line_singlepart_new.gexf')
# create links between nodes
# add metadata of links
# save graph
# release dataset
layer = None
dataSource = None