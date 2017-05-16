# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from osgeo import ogr, osr
import networkx as nx
import numpy as np

#calculate length of StringLine
def calculateGeometryLength(pointList, sourceSRS, destSRS):
    line = ogr.Geometry(ogr.wkbLineString)
    transform = osr.CoordinateTransformation(sourceSRS,destSRS)
    for point in pointList:
        line.AddPoint(point[0],point[1])
    line.Transform(transform)
    return line.Length()

# target srs for road length computation
target_srs = osr.SpatialReference()
target_srs.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs ')

highwayFileName = './roaddata/R_VN_NHW_Inventory.shp'
dataSource = ogr.Open(highwayFileName)
layer = dataSource.GetLayer(0)
source_srs = layer.GetSpatialRef()
featureCount = layer.GetFeatureCount()
print('featureCount: ', featureCount)

# get attribute list
attributeList = []
layerDefinition = layer.GetLayerDefn()
for i in range(layerDefinition.GetFieldCount()):
    fieldName =  layerDefinition.GetFieldDefn(i).GetName()
    attributeList.append(fieldName)

G = nx.Graph()
nodeList = []
i = 0
for feature in layer:
    geometry = feature.geometry()
    geometry.TransformTo(target_srs)
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
    G.add_edge(lastNodeID, firstNodeID)
    for attribute in attributeList:
        G[lastNodeID][firstNodeID][attribute] = feature.GetField(attribute) if feature.GetField(attribute) is not None else ''

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

nx.write_gexf(G,'./R_VN_NHW_Inventory.gexf')

layer = None
dataSource = None
