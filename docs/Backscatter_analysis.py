import rasterio
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def read_sar_data(file_paths):
    """Read and stack multiple SAR images with error handling."""
    stack = []
    metadata = None
    for path in file_paths:
        try:
            with rasterio.open(path) as src:
                data = src.read(1)
                if metadata is None:  # Save metadata from first file
                    metadata = src.meta
                stack.append(data)
        except (FileNotFoundError, rasterio.errors.RasterioIOError) as e:
            raise SystemExit(f"Error reading {path}: {str(e)}")
    return np.stack(stack), metadata

def process_sar_stack(stack):
    """Process SAR data stack with NaN handling and averaging."""
    # Convert to float for calculations
    stack = stack.astype(np.float32)
    
    # Replace zeros with NaNs for better handling
    stack[stack == 0] = np.nan
    
    # Check if we have any valid data in each position
    has_valid_data = np.any(~np.isnan(stack), axis=0)
    
    # Initialize output array filled with zeros
    avg = np.zeros_like(stack[0])
    
    # Only calculate mean where we have valid data
    if np.any(has_valid_data):
        # Suppress the warning by only calculating mean where we have data
        with np.errstate(invalid='ignore'):
            avg[has_valid_data] = np.nanmean(stack[:, has_valid_data], axis=0)
    else:
        print("Warning: No valid data found in the stack")
    
    return avg

def plot_backscatter_hist(pre_data, post_data):
    """Plot comparative histogram with proper SAR formatting."""
    plt.figure(figsize=(12, 6))
    
    # Print data statistics for debugging
    print(f"Pre-flood data - min: {np.min(pre_data)}, max: {np.max(pre_data)}, mean: {np.mean(pre_data)}")
    print(f"Post-flood data - min: {np.min(post_data)}, max: {np.max(post_data)}, mean: {np.mean(post_data)}")
    
    # Filter out non-positive values and zeros for log scaling
    pre_filtered = pre_data.flatten()
    pre_filtered = pre_filtered[pre_filtered > 0]
    
    post_filtered = post_data.flatten()
    post_filtered = post_filtered[post_filtered > 0]
    
    # Print filtered statistics
    print(f"After filtering - Pre-flood count: {len(pre_filtered)}, Post-flood count: {len(post_filtered)}")
    
    # Check if we have valid data after filtering
    if len(pre_filtered) == 0 or len(post_filtered) == 0:
        print("Warning: No positive values found in data for histogram")
        return
    
    # Try using linear bins first to see distribution
    plt.figure(figsize=(12, 6))
    plt.hist(pre_filtered, bins=50, alpha=0.7, 
             color='navy', label='Pre-Flood')
    plt.hist(post_filtered, bins=50, alpha=0.7,
             color='maroon', label='Post-Flood')
    plt.xlabel('Backscatter Intensity (linear scale)')
    plt.ylabel('Pixel Count')
    plt.title('SAR Backscatter Intensity Distribution (Linear): Pre- vs Post-Flood', pad=20)
    plt.legend()
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('backscatter_histogram_linear.png', dpi=300, bbox_inches='tight')
    
    # Now create the log-scale histogram
    plt.figure(figsize=(12, 6))
    
    # Compute histogram ranges with more care
    min_val = min(np.min(pre_filtered), np.min(post_filtered))
    max_val = max(np.max(pre_filtered), np.max(post_filtered))
    
    # Safety check for log binning
    if min_val <= 0:
        min_val = 0.1  # Small positive value
    
    # Create more appropriate bins - try more bins and ensure the range is appropriate
    if max_val / min_val > 1000:  # Large dynamic range
        bins = np.logspace(np.log10(min_val), np.log10(max_val), 100)
    else:  # Smaller dynamic range
        # Maybe the data is in dB already and doesn't need log scale
        bins = np.linspace(min_val, max_val, 100)
    
    # Plot with transparent histograms so both are visible
    plt.hist(pre_filtered, bins=bins, alpha=0.6, 
             color='navy', label='Pre-Flood')
    plt.hist(post_filtered, bins=bins, alpha=0.6,
             color='maroon', label='Post-Flood')
    
    # Only use log scale if appropriate for the data range
    if max_val / min_val > 100:  # Only use log scale for large ranges
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Backscatter Intensity (σ⁰, log scale)')
    else:
        plt.xlabel('Backscatter Intensity (σ⁰, linear scale)')
    
    plt.ylabel('Pixel Count')
    plt.title('SAR Backscatter Intensity Distribution: Pre- vs Post-Flood', pad=20)
    plt.legend()
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('backscatter_histogram.png', dpi=300, bbox_inches='tight')

def plot_difference_map(difference, metadata):
    """Plot calibrated difference map with geographic context."""
    plt.figure(figsize=(12, 8))
    
    # Calculate percentiles for robust color scaling
    # Add error handling for all-NaN arrays
    if np.all(np.isnan(difference)):
        print("Warning: Difference map contains only NaN values")
        return
    
    vmin = np.nanpercentile(difference, 2)
    vmax = np.nanpercentile(difference, 98)
    
    # Create plot with coordinate system
    ax = plt.subplot(111)
    im = ax.imshow(difference, cmap='coolwarm', vmin=vmin, vmax=vmax,
                   extent=[0, metadata['width']*metadata['transform'][0],
                   0, metadata['height']*metadata['transform'][4]])
    
    # Add colorbar with units
    cbar = plt.colorbar(im, fraction=0.046, pad=0.04)
    cbar.set_label('Backscatter Difference (dB)', rotation=270, labelpad=20)
    
    # Add map elements
    plt.title('Flood Impact Difference Map', pad=20)
    plt.xlabel('Easting (m)')
    plt.ylabel('Northing (m)')
    plt.grid(linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig('difference_map.png', dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    # Configuration
    DATA_DIR = Path("E:/FLOOD/SAR_IMAGES")
    
    # File paths using pathlib for Windows compatibility
    pre_flood_files = [
        DATA_DIR / "subset_0_of_S1A_IW_GRDH_1SDV_20240806_tnr_Orb_Bdr_Cal_Spk_TC_Stack_Flood_Mask_6Aug.tif",
        DATA_DIR / "subset_0_of_S1A_IW_GRDH_1SDV_20240806_tnr_Orb_Bdr_Cal_Spk_TC_Stack_Flood_Mask_18Aug.tif"
    ]
    
    post_flood_files = [
        DATA_DIR / "subset_0_of_S1A_IW_GRDH_1SDV_20240806_tnr_Orb_Bdr_Cal_Spk_TC_Stack_WATER_FLOOD.tif",
        DATA_DIR / "subset_0_of_S1A_IW_GRDH_1SDV_20240806_tnr_Orb_Bdr_Cal_Spk_TC_Stack_flood_Mask_23Sep.tif"
    ]

    # Data processing pipeline
    pre_stack, meta = read_sar_data(pre_flood_files)
    post_stack, _ = read_sar_data(post_flood_files)
    
    pre_avg = process_sar_stack(pre_stack)
    post_avg = process_sar_stack(post_stack)
    
    # Generate difference map (Post - Pre)
    difference = post_avg - pre_avg
    
    # Visualization
    plot_backscatter_hist(pre_avg, post_avg)
    plot_difference_map(difference, meta)
