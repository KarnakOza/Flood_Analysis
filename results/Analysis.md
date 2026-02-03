## Preliminary Analysis

- Observations from SAR-Based Flood Mapping.
- Preliminary observations indicate a clear contrast between flooded and non-flooded areas, with backscatter values significantly decreasing over water surfaces due to the smooth reflection of radar signals.
- VV Polarization Observations
- Lower backscatter values over flooded regions, making water bodies appear darker.
- More effective in detecting open water areas compared to vegetated regions.
  
![image alt](https://github.com/KarnakOza/Flood_Analysis/blob/0e0c34c45510b6919dab109c573988562167e109/figures/backscatter_histogram.png)


As seen the drop of backscatter intensity from pre to post.

![image alt](https://github.com/KarnakOza/Flood_Analysis/blob/0e0c34c45510b6919dab109c573988562167e109/figures/backscatter_histogram_linear.png)


**VV + VH Polarization**
- VV - Sensitive to open water (specular reflection).
- VH - Detects flooded vegetation (volume scattering).

# Practical Implications

•	Post-flood backscatter suppression: VV dropped by 6.4 dB, VH by 5.6 dB, consistent with specular reflection over water.

•	Cross-pol ratio increase: VH/VV rose from 0.32 → 0.41, suggesting double-bounce scattering (e.g., flooded vegetation).


![image alt](https://github.com/KarnakOza/Flood_Analysis/blob/c7f77367419c9ef70c49723c56df8c8d31caacd9/figures/segmentation.png) 
