## Workflow

Sentinel-1 SAR preprocessing in ESA SNAP INCLUDED:
(1) Thermal Noise Removal using LUTs;
(2) orbit correction with precise files;
(3) Border Noise Removal (500px margin, threshold=0.5);
(4) Radiometric Correction to Sigma Naught;
(5) Lee Sigma speckle filtering (7x7 window);
(6) Terrain correction via SRTM-3Sec DEM (bilinear interpolation);and 
(7) band math for water mask generation, to ensure accurate flood boundary delineation.


## Flow-Chart
![image alt](https://github.com/KarnakOza/Flood_Analysis/blob/5858dedf433bd802c7a1bd34ccfe8954a0887ba8/methodology/Sentinel-1A%20C%20Band%20VV%26VH%20IW_GRDH_1S.png)
