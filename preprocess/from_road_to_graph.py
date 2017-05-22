#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 17:32:10 2017

@author: giangblackk
"""

from osgeo import ogr, osr
import networkx as nx
import numpy as np

def calculateGeometryLength(pointList, sourceSRS, destSRS):
    line = ogr.Geometry(ogr.wkbLineString)
    transform = osr.CoordinateTransformation(sourceSRS,destSRS)
    for point in pointList:
        line.AddPoint(point[0],point[1])
    line.Transform(transform)
    return line.Length()

# target srs for road length computation
target_srs = osr.SpatialReference()
target_srs.ImportFromProj4('+proj=utm +zone=48 +ellps=WGS84 +datum=WGS84 +units=m +no_defs ')

# read source dataset
highwayFileName = './roaddata/highway_line_singlepart.shp'
dataSource = ogr.Open(highwayFileName)
layer = dataSource.GetLayer(0)
source_srs = layer.GetSpatialRef()
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
nodeList = []
i = 0

for feature in layer:
    geometry = feature.geometry()
    geometry_projected = geometry.Clone()
    geometry_projected.TransformTo(target_srs)
    feature_length = geometry_projected.Length()
    pointCount = geometry.GetPointCount()
    pointList = geometry.GetPoints()
    ### first point ###########################################################
    firstPoint = pointList[0]
    if not firstPoint in nodeList:
        nodeList.append(firstPoint)
        G.add_node(i, lng=firstPoint[0], lat=firstPoint[1])
        firstNodeID = i
        i = i + 1
    else:
        for nodeidx in G.nodes_iter():
            if G.node[nodeidx]['lng'] == firstPoint[0] and G.node[nodeidx]['lat'] == firstPoint[1]:
                firstNodeID = nodeidx
    
    ### last point ############################################################
    lastPoint = pointList[-1]
    if not lastPoint in nodeList:
        nodeList.append(lastPoint)
        G.add_node(i, lng=lastPoint[0], lat=lastPoint[1])
        lastNodeID = i
        i = i + 1
    else:
        for nodeidx in G.nodes_iter():
            if G.node[nodeidx]['lng'] == lastPoint[0] and G.node[nodeidx]['lat'] == lastPoint[1]:
                lastNodeID = nodeidx
    
    ### if first point is same as last point, remove due to loop ##############
    if firstNodeID == lastNodeID or firstPoint == lastPoint:
        G.remove_node(firstNodeID)
        nodeList.remove(firstPoint)
        continue
    ### add edges between nodes ###############################################
    middlePointList = pointList[1:-1]
    if firstNodeID in middlePointList or lastNodeID in middlePointList:
#        G.remove_node(firstNodeID)
#        nodeList.remove(firstPoint)
#        G.remove_node(lastNodeID)
#        nodeList.remove(lastPoint)
        continue
    ### create link ###########################################################
    if feature.GetField('ONEWAY') == '-1':
        G.add_edge(lastNodeID, firstNodeID)
        for attribute in attributeList:
            G[lastNodeID][firstNodeID][attribute] = feature.GetField(attribute) if feature.GetField(attribute) is not None else ''
        G[lastNodeID][firstNodeID]['middle'] = middlePointList[::-1]
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
        G[lastNodeID][firstNodeID]['middle'] = middlePointList[::-1]
        G[firstNodeID][lastNodeID]['length'] = feature_length
        G[lastNodeID][firstNodeID]['length'] = feature_length
    ### intersect processing ##################################################
    for edge in G.edges():
        headID = edge[0]
        tailID = edge[1]
        attributeDict = G[headID][tailID]
        middle = attributeDict['middle']
        if firstPoint in middle:
            if headID == firstNodeID or firstNodeID == tailID:
                continue
            indexFirstPoint = middle.index(firstPoint)
            # copy attributes
            attributeDictPart1 = attributeDict.copy()
            attributeDictPart2 = attributeDict.copy()
            # recalculate middle
            attributeDictPart1['middle'] = middle[0:indexFirstPoint]
            attributeDictPart2['middle'] = middle[indexFirstPoint+1:]
            # recalucate length
            roadPart1 = [(G.node[headID]['lng'],G.node[headID]['lat'])]
            roadPart1.extend(middle[0:indexFirstPoint+1])
            roadPart2 = middle[indexFirstPoint:]
            roadPart2.append((G.node[tailID]['lng'],G.node[tailID]['lat']))
            attributeDictPart1['length'] = calculateGeometryLength(roadPart1,source_srs,target_srs)
            attributeDictPart2['length'] = calculateGeometryLength(roadPart2,source_srs,target_srs)
            G.remove_edge(headID, tailID)
            G.add_edge(headID, firstNodeID, attr_dict=attributeDictPart1)
            G.add_edge(firstNodeID, tailID, attr_dict=attributeDictPart2)
        elif lastPoint in middle:
            if headID == lastNodeID or lastNodeID == tailID:
                continue
            indexLastPoint = middle.index(lastPoint)
            # copy attributes
            attributeDictPart1 = attributeDict.copy()
            attributeDictPart2 = attributeDict.copy()
            # recalculate middle
            attributeDictPart1['middle'] = middle[0:indexLastPoint]
            attributeDictPart2['middle'] = middle[indexLastPoint+1:]
            # recalculate length
            roadPart1 = [(G.node[headID]['lng'],G.node[headID]['lat'])]
            roadPart1.extend(middle[0:indexLastPoint+1])
            roadPart2 = middle[indexLastPoint:]
            roadPart2.append((G.node[tailID]['lng'],G.node[tailID]['lat']))
            attributeDictPart1['length'] = calculateGeometryLength(roadPart1,source_srs,target_srs)
            attributeDictPart2['length'] = calculateGeometryLength(roadPart2,source_srs,target_srs)
            G.remove_edge(headID, tailID)
            G.add_edge(headID, lastNodeID, attr_dict=attributeDictPart1)
            G.add_edge(lastNodeID, tailID, attr_dict=attributeDictPart2)

### remove middle properties ##################################################
for edge in G.edges_iter():
    G[edge[0]][edge[1]].pop('middle')

### remove zeros neighbor nodes ###############################################
for node in G.nodes():
    if G.in_degree()[node] == 0 and G.out_degree()[node] == 0:
        print(node)
        G.remove_node(node)
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
# nx.write_gexf(G,'./highway_line_singlepart_new_length.gexf')
# nx.write_gexf(G,'./highway_line_singlepart_new_123.gexf')
nx.write_gexf(G,'./graphdata/highway_line_singlepart_new_length.gexf')
# create links between nodes
# add metadata of links
# save graph
# release dataset
layer = None
dataSource = None