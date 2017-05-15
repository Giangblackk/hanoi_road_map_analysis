#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 17:32:10 2017

@author: giangblackk
"""

from osgeo import ogr, osr
import networkx as nx
import numpy as np

# read source dataset
highwayFileName = './highway_line_singlepart.shp'
dataSource = ogr.Open(highwayFileName)
layer = dataSource.GetLayer(0)
spatialRef = layer.GetSpatialRef()
featureCount = layer.GetFeatureCount()
print('featureCount: ', featureCount)
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
self_loop_count = 0
for feature in layer:
    geometry = feature.geometry()
    geometry_projected = geometry.Clone()
    target_srs = osr.SpatialReference()
    target_srs.ImportFromProj4('+proj=utm +zone=48 +ellps=WGS84 +datum=WGS84 +units=m +no_defs ')
    geometry_projected.TransformTo(target_srs)
    feature_length = geometry_projected.Length()
    pointCount = geometry.GetPointCount()
    ### first point ###########################################################
    firstPoint = (geometry.GetPoint(0)[0],geometry.GetPoint(0)[1])
    if not firstPoint in pointList:
        pointList.append(firstPoint)
        G.add_node(i, lng=firstPoint[0], lat=firstPoint[1])
        firstNodeID = i
        i = i + 1
    else:
        for nodeidx in G.nodes_iter():
            if G.node[nodeidx]['lng'] == firstPoint[0] and G.node[nodeidx]['lat'] == firstPoint[1]:
                firstNodeID = nodeidx
    
    ### last point ############################################################
    lastPoint = (geometry.GetPoint(pointCount-1)[0], geometry.GetPoint(pointCount-1)[1])
    if not lastPoint in pointList:
        pointList.append(lastPoint)
        G.add_node(i, lng=lastPoint[0], lat=lastPoint[1])
        lastNodeID = i
        i = i + 1
    else:
        for nodeidx in G.nodes_iter():
            if G.node[nodeidx]['lng'] == lastPoint[0] and G.node[nodeidx]['lat'] == lastPoint[1]:
                lastNodeID = nodeidx
    
    ### if first point is same as last point, remove due to loop ##############
    if firstNodeID == lastNodeID or firstPoint == lastPoint:
        continue
    
    ### add edges between nodes ###############################################
    middlePointList = []
    for j in range(1,pointCount-1):
        middlePointList.append((geometry.GetPoint(j)[0], geometry.GetPoint(j)[1]))
    
    ### create link ###########################################################
    if feature.GetField('ONEWAY') == '-1':
        G.add_edge(lastNodeID, firstNodeID)
        for attribute in attributeList:
            G[lastNodeID][firstNodeID][attribute] = feature.GetField(attribute) if feature.GetField(attribute) is not None else ''
        G[lastNodeID][firstNodeID]['middle'] = middlePointList
        G[lastNodeID][firstNodeID]['length'] = feature_length
    elif feature.GetField('ONEWAY') == 'yes':
        G.add_edge(firstNodeID, lastNodeID)
        for attribute in attributeList:
            G[firstNodeID][lastNodeID][attribute] = feature.GetField(attribute) if feature.GetField(attribute) is not None else ''
        G[firstNodeID][lastNodeID]['middle'] = middlePointList
        G[firstNodeID][lastNodeID]['length'] = feature_length
    else:
        G.add_edge(firstNodeID, lastNodeID)
        G.add_edge(lastNodeID, firstNodeID)
        for attribute in attributeList:
            G[firstNodeID][lastNodeID][attribute] = feature.GetField(attribute) if feature.GetField(attribute) is not None else ''
            G[lastNodeID][firstNodeID][attribute] = feature.GetField(attribute) if feature.GetField(attribute) is not None else ''
        G[firstNodeID][lastNodeID]['middle'] = middlePointList
        G[lastNodeID][firstNodeID]['middle'] = middlePointList
        G[firstNodeID][lastNodeID]['length'] = feature_length
        G[lastNodeID][firstNodeID]['length'] = feature_length
    ### intersect processing ##################################################
    edges = G.edges()
    for edge in edges:
        headID = edge[0]
        tailID = edge[1]
        middle = G[headID][tailID]['middle']
        if firstPoint in middle:
            if headID == firstNodeID or firstNodeID == tailID:
                continue
            attributeDict = G[headID][tailID]
            G.remove_edge(headID, tailID)
            G.add_edge(headID, firstNodeID, attr_dict=attributeDict)
            G.add_edge(firstNodeID, tailID, attr_dict=attributeDict)
        elif lastPoint in middle:
            if headID == lastNodeID or lastNodeID == tailID:
                continue
            attributeDict = G[headID][tailID]
            G.remove_edge(headID, tailID)
            G.add_edge(headID, lastNodeID, attr_dict=attributeDict)
            G.add_edge(lastNodeID, tailID, attr_dict=attributeDict)

### remove middle properties ##################################################
for edge in G.edges_iter():
    G[edge[0]][edge[1]].pop('middle')

### check if 2 node same lat long #############################################
lat = G.node[0]['lat']
lng = G.node[0]['lng']
sameCount = -1
for i in G.nodes_iter():
    if G.node[i]['lat'] == lat and G.node[i]['lng'] == lng:
        sameCount += 1
    else:
        lat = G.node[i]['lat']
        lng = G.node[i]['lng']
print('same location Count: ',sameCount)

### check for self loop in result graph #######################################
self_loop_count = 0
for node in G.nodes_iter():
    if node in G.neighbors(node):
        self_loop_count += 1
        print(node, G.neighbors(node))
print('self_loop_count: ', self_loop_count)

# nx.write_gexf(G,'./highway_line_singlepart.gexf')
nx.write_gexf(G,'./highway_line_singlepart_new_length.gexf')
# nx.write_gexf(G,'./highway_line_singlepart_new_123.gexf')
# create links between nodes
# add metadata of links
# save graph
# release dataset
layer = None
dataSource = None