import ee, leafmap
ee.Initialize()

# Region: Alberta
canada = ee.FeatureCollection('FAO/GAUL/2015/level1')
alberta = canada.filter(ee.Filter.eq('ADM1_NAME', 'Alberta'))

# Datasets
worldcover = ee.Image('ESA/WorldCover/v200').select('Map')
hansen = ee.Image('UMD/hansen/global_forest_change_2023_v1_11')
viirs = ee.ImageCollection('NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG') \
    .filterDate('2023-01-01', '2023-12-31') \
    .select('avg_rad').mean()
wdpa = ee.FeatureCollection('WCMC/WDPA/current/polygons')

# Masks
cropland = worldcover.eq(40)
builtup = worldcover.eq(50)
forest = worldcover.eq(10)
protected = wdpa.filterBounds(alberta).reduceToImage(['REP_AREA'], ee.Reducer.first()).gt(0)
night = viirs.gt(5)

# Exclusion
used = cropland.Or(builtup).Or(forest).Or(protected).Or(night)
lowuse = used.Not().updateMask(alberta)

# Visualization
Map = leafmap.Map(center=[55, -115], zoom=5)
Map.addLayer(worldcover, {}, 'WorldCover 2023')
Map.addLayer(lowuse, {'palette': ['white','green']}, 'Low-use Areas')
Map.addLayerControl()
Map
