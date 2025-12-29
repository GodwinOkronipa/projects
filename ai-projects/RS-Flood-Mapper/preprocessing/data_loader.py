# preprocessing/data_loader.py

import rasterio
import numpy as np

def load_geotiff(filepath):
    """
    Loads a GeoTIFF file into a NumPy array.

    Args:
        filepath (str): The path to the .tif file.

    Returns:
        numpy.ndarray: The image data as a NumPy array.
        dict: The metadata of the GeoTIFF file (e.g., transform, crs).
    """
    try:
        with rasterio.open(filepath) as src:
            image = src.read()
            meta = src.meta
            # If the image has a single band, return a 2D array
            if image.shape[0] == 1:
                image = image.squeeze()
            return image, meta
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None, None