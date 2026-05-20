import os
import numpy as np
import rasterio
import argparse


def preprocess_raster(input_data):
    with rasterio.open(input_data) as src:
        input_data = src.read()
        profile = src.profile
        input_data = np.moveaxis(input_data, 0, -1)

    return input_data, profile


def get_sorted_tif_paths(input_folder):
    input_paths = sorted([
        os.path.join(input_folder, fname)
        for fname in os.listdir(input_folder)
        if fname.endswith(".tif")
    ])
    return input_paths


def colorize_image(input_path, output_raster):
    input_data, profile = preprocess_raster(input_path)

    # Create RGB image initialized as white
    height, width, _ = input_data.shape
    rgb_image = np.ones((height, width, 3), dtype=np.uint8) * 255  # Start with white

    # Set turquoise color for pixels with value 1
    turquoise_color = np.array([64, 224, 208], dtype=np.uint8)

    # Assume we are using the first band to check pixel values
    mask = input_data[..., 0] == 1  # Only pixels with value 1

    rgb_image[mask] = turquoise_color

    # Update profile for 3-band RGB output
    profile.update(count=3, dtype=rasterio.uint8)

    with rasterio.open(output_raster, 'w', **profile) as dst:
        for i in range(3):
            dst.write(rgb_image[:, :, i], i + 1)

    print(f"Colorized raster saved to {output_raster}.")


def colorize_images(input_data_paths):
    output_dir = "output_colorized"
    os.makedirs(output_dir, exist_ok=True)

    for file_idx, input_path in enumerate(input_data_paths):
        print(f"Colorizing the file: {input_path}")

        file_name = os.path.basename(input_path)
        output_path = os.path.join(output_dir, file_name)
        colorize_image(input_path, output_path)


# ========== ARGPARSE ==========
parser = argparse.ArgumentParser(description="Colorize binary rasters: 0→white, 1→turquoise.")
parser.add_argument("--path", type=str, default="output_threshold_0.9", help="Path to folder containing binary rasters.")

args = parser.parse_args()

# ========== CONFIGURATION ==========
PATH = args.path

# ========== FOLDER PATHS ==========
DATA_DIR = "."
path_label_dir = os.path.join(DATA_DIR, PATH)

# ========== LOAD PATHS ==========
print("Loading paths...")
input_paths = get_sorted_tif_paths(path_label_dir)

colorize_images(input_paths)
