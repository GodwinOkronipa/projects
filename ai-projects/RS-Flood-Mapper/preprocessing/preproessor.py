# preprocessing/preprocessor.py

import numpy as np
from scipy.ndimage import median_filter

def apply_speckle_filter(sar_image, filter_size=3):
    """
    Applies a simple median filter to a SAR image to reduce speckle noise.

    Args:
        sar_image (numpy.ndarray): The input SAR image (single band).
        filter_size (int): The size of the median filter window.

    Returns:
        numpy.ndarray: The filtered SAR image.
    """
    print(f"Applying median speckle filter with size {filter_size}...")
    return median_filter(sar_image, size=filter_size)


def normalize_image(image):
    """
    Normalizes image pixel values to be between 0 and 1.

    Args:
        image (numpy.ndarray): The input image (can be multi-band).

    Returns:
        numpy.ndarray: The normalized image.
    """
    print("Normalizing image to range [0, 1]...")
    min_val = np.min(image)
    max_val = np.max(image)
    
    if max_val - min_val > 0:
        return (image - min_val) / (max_val - min_val)
    else:
        # Return a zero array if the image is flat
        return np.zeros_like(image)

def calculate_ndwi(s2_image, green_band_idx=1, nir_band_idx=7):
    """
    Calculates the Normalized Difference Water Index (NDWI).
    NDWI = (Green - NIR) / (Green + NIR)
    
    Note: Band indices are based on common Sentinel-2 band ordering. Adjust if needed.
    Band 3 (Green) -> index 1
    Band 8 (NIR) -> index 7

    Args:
        s2_image (numpy.ndarray): Sentinel-2 image with shape (bands, height, width).
        green_band_idx (int): The index for the Green band.
        nir_band_idx (int): The index for the Near-Infrared (NIR) band.

    Returns:
        numpy.ndarray: A 2D array representing the NDWI.
    """
    print("Calculating NDWI...")
    green = s2_image[green_band_idx, :, :].astype(float)
    nir = s2_image[nir_band_idx, :, :].astype(float)
    
    # Use np.errstate to avoid division by zero warnings
    with np.errstate(divide='ignore', invalid='ignore'):
        ndwi = (green - nir) / (green + nir)
    
    # Replace NaN or Inf values with 0
    ndwi[~np.isfinite(ndwi)] = 0
    return ndwi