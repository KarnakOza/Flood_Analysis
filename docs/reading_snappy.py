path_to_sentinel_data = "File_path.zip"
product = ProductIO.readProduct(path_to_sentinel_data)

#Reading the zip file
##To get width and height band_name info
  
width = product.getSceneRasterWidth()
print("Width: {} px".format(width))
height = product.getSceneRasterHeight()
print("Height: {} px".format(height))
name = product.getName()
print("Name: {}".format(name))
band_names = product.getBandNames()
print("Band names: {}".format(", ".join(band_names)))

#Product In-line

def plotBand(product, band, vmin, vmax):
band = product.getBand(band)
w = band.getRasterWidth()
h = band.getRasterHeight()
print(w, h)
band_data = np.zeros(w * h, np.float32)
band.readPixels(0, 0, w, h, band_data)
band_data.shape = h, w
width = 12
height = 12
plt.figure(figsize=(width, height))
imgplot = plt.imshow(band_data, cmap=plt.cm.binary, vmin=vmin, vmax=vmax)


##Applying Orbit File 
parameters = HashMap()
GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
parameters.put('orbitType', 'Sentinel Precise (Auto Download)')
parameters.put('polyDegree', '3')
parameters.put('continueOnFail', 'false')
apply_orbit_file = GPF.createProduct('Apply-Orbit-File', parameters, product)
return imgplot

##Subsetting the product by utilizing the shp of the city if it falls under AOI or merging and clipping of shp.
##Skipable task

r = shapefile.Reader("data/island_boundary2.shp")
g=[]
for s in r.shapes():
g.append(pygeoif.geometry.as_shape(s))
m = pygeoif.MultiPoint(g)
wkt = str(m.wkt).replace("MULTIPOINT", "POLYGON(") + ")"
SubsetOp = snappy.jpy.get_type('org.esa.snap.core.gpf.common.SubsetOp')
bounding_wkt = wkt
geometry = WKTReader().read(bounding_wkt)
HashMap = snappy.jpy.get_type('java.util.HashMap')
GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
parameters = HashMap()
parameters.put('copyMetadata', True)
parameters.put('geoRegion', geometry)
product_subset = snappy.GPF.createProduct('Subset', parameters,
apply_orbit_file)



