import os
import hashlib
import shutil

def file_hash(filepath):
    """Generate MD5 hash for a file."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def collect_unique_images(source_folders, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    seen_hashes = set()
    counter = 2215

    for folder in source_folders:
        for root, _, files in os.walk(folder):
            for file in files:
                filepath = os.path.join(root, file)
                filehash = file_hash(filepath)

                if filehash not in seen_hashes:
                    seen_hashes.add(filehash)
                    counter += 1
                    # Preserve file extension
                    ext = os.path.splitext(file)[1]
                    new_filename = f"image_{counter}{ext}"
                    shutil.copy2(filepath, os.path.join(destination_folder, new_filename))

    print(f"✅ Done! Collected {counter} unique images into {destination_folder}")

# Example usage:
source_folders = [
    "dataset/целостность/битый/datasettt_val/1",
    "dataset/целостность/битый/datasettt_val/3",
    "dataset/целостность/битый/datasettt_val/4",
    "dataset/целостность/битый/datasettt_val/5"
]
destination_folder = "dataset/целостность/битый/all_dent"

collect_unique_images(source_folders, destination_folder)