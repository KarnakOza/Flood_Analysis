# Function to load TIF image safely
def load_tif_image(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} was not found. Please verify the file location.")

    with rasterio.open(file_path) as src:
        data = src.read(1).astype(np.float32)
        data = np.where(data == src.nodata, np.nan, data)  # Handle NoData values
    return data

# File Paths
files = {
    "Flood Mask 6 Aug"  : "subset_0_of_S1A_IW_GRDH_1SDV_20240806_tnr_Orb_Bdr_Cal_Spk_TC_Stack_Flood_Mask_6Aug.tif",
    "Flood Mask 18 Aug" : "subset_0_of_S1A_IW_GRDH_1SDV_20240806_tnr_Orb_Bdr_Cal_Spk_TC_Stack_Flood_Mask_18Aug.tif",
    "Water Flood"       : "subset_0_of_S1A_IW_GRDH_1SDV_20240806_tnr_Orb_Bdr_Cal_Spk_TC_Stack_WATER_FLOOD.tif",
    "Flood Mask 23 Sep" : "subset_0_of_S1A_IW_GRDH_1SDV_20240806_tnr_Orb_Bdr_Cal_Spk_TC_Stack_flood_Mask_23Sep.tif"
}

# Load DEM data
dem_data_list = {name: load_tif_image(path) for name, path in files.items()}

# Compute mean elevations
mean_elevations = {name: np.nanmean(data) for name, data in dem_data_list.items()}

# **1. Boxplot of Mean Elevation**
plt.figure(figsize=(6, 4))
plt.boxplot(list(mean_elevations.values()), vert=True, patch_artist=True, 
            boxprops=dict(facecolor='lightblue'), medianprops=dict(color='red'))
plt.xticks([1], ["Mean Elevation"])
plt.ylabel("Elevation (m)")
plt.title("Elevation Mean Boxplot")
plt.grid(True)
plt.show()

# **2. Mean Elevation Distribution Histogram**
plt.figure(figsize=(8, 5))
plt.hist(list(mean_elevations.values()), bins=10, color="blue", alpha=0.7)
plt.xlabel("Mean Elevation (m)")
plt.ylabel("Frequency")
plt.title("Mean Elevation Distribution")
plt.grid(True)
plt.show()

# Print mean elevations
for name, mean_elev in mean_elevations.items():
    print(f"{name}: Mean Elevation = {mean_elev:.2f} m")
