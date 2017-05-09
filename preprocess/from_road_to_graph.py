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
layer.SetAttributeFilter("ONEWAY NOT IN ('-1','no','yes')")
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
#    print(firstNodeID,lastNodeID)
#    middlePointList = []
#    for j in range(1,pointCount-1):
#        middlePointList.append((geometry.GetPoint(j)[0], geometry.GetPoint(j)[1]))
#    if feature.GetField('ONEWAY') == '-1':
#        roadList.append({'first':lastNodeID,'last':firstNodeID,'middle':middlePointList})
#    elif feature.GetField('ONEWAY') == 'yes':
#        roadList.append({'first':firstNodeID,'last':lastNodeID,'middle':middlePointList})
#    else:
#        roadList.append({'first':firstNodeID,'last':lastNodeID,'middle':middlePointList})
#        roadList.append({'first':lastNodeID,'last':firstNodeID,'middle':middlePointList})
    # check if last or first point in on other road
###############################################################################
    for road in roadList:
        if firstPoint in road['middle']:
            # print('head_intersect')
            firstRoadID = road['first']
            lastRoadID = road['last']
#            print(G.node[firstRoadID])
#            print(G.node[lastRoadID])
#            print(firstRoadID,lastRoadID)
#            print(G.edges())
#            print(G.neighbors(firstRoadID))
#            print(G.neighbors(lastRoadID))
            attributeDict = G[firstRoadID][lastRoadID]
            G.remove_edge(firstRoadID, lastRoadID)
            G.add_edge(firstRoadID, firstNodeID, attr_dict=attributeDict)
            G.add_edge(firstNodeID, lastRoadID, attr_dict=attributeDict)
            roadList.remove(road)
        elif lastPoint in road['middle']:
            # print('tail_intersect')
            firstRoadID = road['first']
            lastRoadID = road['last']
#            print(firstRoadID,lastRoadID)
#            print(G.edges())
            attributeDict = G[firstRoadID][lastRoadID]
            G.remove_edge(firstRoadID, lastRoadID)
            G.add_edge(firstRoadID, lastNodeID, attr_dict=attributeDict)
            G.add_edge(lastNodeID, lastRoadID, attr_dict=attributeDict)
            roadList.remove(road)
###############################################################################
    # create link
    if feature.GetField('ONEWAY') == '-1':
        G.add_edge(lastNodeID, firstNodeID)
        for attribute in attributeList:
            G[lastNodeID][firstNodeID][attribute] = feature.GetField(attribute) if feature.GetField(attribute) is not None else ''
    elif feature.GetField('ONEWAY') == 'yes':
        G.add_edge(firstNodeID, lastNodeID)
        for attribute in attributeList:
            G[firstNodeID][lastNodeID][attribute] = feature.GetField(attribute) if feature.GetField(attribute) is not None else ''
    else:
        G.add_edge(firstNodeID, lastNodeID)
        G.add_edge(lastNodeID, firstNodeID)
        for attribute in attributeList:
            G[firstNodeID][lastNodeID][attribute] = feature.GetField(attribute) if feature.GetField(attribute) is not None else ''
            G[lastNodeID][firstNodeID][attribute] = feature.GetField(attribute) if feature.GetField(attribute) is not None else ''
    # add to roadList
    middlePointList = []
    for j in range(1,pointCount-1):
        middlePointList.append((geometry.GetPoint(j)[0], geometry.GetPoint(j)[1]))
    if feature.GetField('ONEWAY') == '-1':
        roadList.append({'first':lastNodeID,'last':firstNodeID,'middle':middlePointList})
    elif feature.GetField('ONEWAY') == 'yes':
        roadList.append({'first':firstNodeID,'last':lastNodeID,'middle':middlePointList})
    else:
        roadList.append({'first':firstNodeID,'last':lastNodeID,'middle':middlePointList})
        roadList.append({'first':lastNodeID,'last':firstNodeID,'middle':middlePointList})
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
nx.write_gexf(G,'./highway_line_singlepart_0123.gexf')
# create links between nodes
# add metadata of links
# save graph
# release dataset
layer = None
dataSource = None