import os
from PIL import Image

# Path to your source folder with images
source_folder = "dataset/чистота/dirty"

# Path to your destination folder
dest_folder = "dataset/чистота/dirtyjpeg"
os.makedirs(dest_folder, exist_ok=True)  # create if doesn't exist

# Loop through all files in the source folder
for filename in os.listdir(source_folder):
    file_path = os.path.join(source_folder, filename)
    
    # Only process files that are images
    try:
        with Image.open(file_path) as img:
            # Convert image to RGB (important for formats like PNG with alpha)
            rgb_img = img.convert("RGB")
            
            # Prepare destination path with .jpeg extension
            dest_path = os.path.join(dest_folder, os.path.splitext(filename)[0] + ".jpeg")
            
            # Save as JPEG
            rgb_img.save(dest_path, "JPEG")
            print(f"Converted {filename} -> {dest_path}")
    except Exception as e:
        print(f"Skipping {filename}: {e}")