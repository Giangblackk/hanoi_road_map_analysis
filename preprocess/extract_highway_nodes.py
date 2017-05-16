from osgeo import ogr

highwayFileName = './highway_line_singlepart.shp'

dataSource = ogr.Open(highwayFileName)
layer = dataSource.GetLayer(0)
spatialRef = layer.GetSpatialRef()
featureCount = layer.GetFeatureCount()

outputFileName = './extract/highway_line_intersect.shp'
outDriver = ogr.GetDriverByName('ESRI Shapefile')
outDataSource = outDriver.CreateDataSource(outputFileName)

outLayer = outDataSource.CreateLayer('highway', spatialRef, ogr.wkbPoint)
featureDefn = outLayer.GetLayerDefn()

nodeList = []
for i in range(featureCount):
    feature = layer.GetFeature(i)
    geometry = feature.geometry()
    pointCount = geometry.GetPointCount()
    firstPoint = ogr.Geometry(ogr.wkbPoint)
    lastPoint = ogr.Geometry(ogr.wkbPoint)
    lastPoint.AddPoint(geometry.GetPoint(pointCount-1)[0],geometry.GetPoint(pointCount-1)[1])
    firstPoint.AddPoint(geometry.GetPoint(0)[0],geometry.GetPoint(0)[1])
    if (geometry.GetPoint(pointCount-1)[0],geometry.GetPoint(pointCount-1)[1]) not in nodeList:
        nodeList.append((geometry.GetPoint(pointCount-1)[0],geometry.GetPoint(pointCount-1)[1]))
        outFeature = ogr.Feature(featureDefn)
        outFeature.SetGeometry(firstPoint)
        outLayer.CreateFeature(outFeature)
    if (geometry.GetPoint(0)[0],geometry.GetPoint(0)[1]) not in nodeList:
        nodeList.append((geometry.GetPoint(0)[0],geometry.GetPoint(0)[1]))
        outFeature = ogr.Feature(featureDefn)
        outFeature.SetGeometry(lastPoint)
        outLayer.CreateFeature(outFeature)
#    print('firstPoint: ',firstPoint)
#    print('lastPoint:', lastPoint)
#    nodeList.add((geometry.GetPoint(pointCount-1)[0],geometry.GetPoint(pointCount-1)[1]))
#    nodeList.add((geometry.GetPoint(0)[0],geometry.GetPoint(0)[1]))

print(len(nodeList))

outLayer = None
outDataSource = None
layer = None
dataSource = None