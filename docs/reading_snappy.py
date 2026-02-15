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
return imgplot
