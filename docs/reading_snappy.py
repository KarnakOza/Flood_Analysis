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
