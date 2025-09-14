import os
from PIL import Image

def crop_into_4(img_path, dest_folder, counter_start=0):
    """Crop image into 4 equal parts and save them."""
    img = Image.open(img_path)
    w, h = img.size
    half_w, half_h = w // 2, h // 2

    crops = [
        (0, 0, half_w, half_h),        # top-left
        (half_w, 0, w, half_h),        # top-right
        (0, half_h, half_w, h),        # bottom-left
        (half_w, half_h, w, h)         # bottom-right
    ]

    base_name = os.path.splitext(os.path.basename(img_path))[0]
    ext = ".jpg"  # save all as jpg (can change if you want original)

    for i, box in enumerate(crops, 1):
        cropped = img.crop(box)
        # Convert RGBA → RGB if needed
        if cropped.mode in ("RGBA", "LA"):
            cropped = cropped.convert("RGB")
        out_path = os.path.join(dest_folder, f"{base_name}_part{i}{ext}")
        cropped.save(out_path, "JPEG")

    return 4  # number of crops saved

def process_folders(source_folders, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    count = 0
    for folder in source_folders:
        for file in os.listdir(folder):
            if file.lower().endswith(('mpo', 'dng', 'bmp', 'tif', 'jpg', 'tiff', 'pfm', 'jpeg', 'heic', 'webp', 'png')):
                img_path = os.path.join(folder, file)
                count += crop_into_4(img_path, dest_folder, count)

    print(f"✅ Done! Created {count} cropped images in {dest_folder}")

# Example usage
source_folders = ["dataset/целостность/небитый/yolo_clean", "dataset/целостность/небитый/yolo_dirt"]
destination_folder = "dataset/целостность/небитый/cropped"

process_folders(source_folders, destination_folder)