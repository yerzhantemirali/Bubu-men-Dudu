import json
import pandas as pd


with open("annotations/instances_val2017.json", "r", encoding="utf-8") as f:
    data = json.load(f)

annotations_df = pd.DataFrame(data["annotations"])
annotations_df.drop(columns = ["bbox", "iscrowd", "attributes", "area", "segmentation"], inplace = True)
grouped = annotations_df.groupby("image_id")["category_id"].apply(list).reset_index()
df_grouped = grouped.set_index("image_id")


import os
import shutil
import pandas as pd

# === Пути ===
csv_path = "annotations_grouped.csv"   # твой csv с image_id,category_id
images_dir = "val2017"                  # папка где лежат исходные картинки
output_dir = "datasettt_val"                 # куда складывать по категориям

# Загружаем CSV
df = df_grouped.reset_index()

# Разворачиваем списки (каждый image_id–category_id в отдельной строке)
df = df.explode("category_id")

# Теперь безопасно приводим к int
df["category_id"] = df["category_id"].astype(int)

# Разворачиваем (каждая пара image_id–category_id в отдельной строке)
df = df.explode("category_id")
df["category_id"] = df["category_id"].astype(int)

# Переносим изображения
for _, row in df.iterrows():
    img_id = row["image_id"]
    cat_id = row["category_id"]

    # имя файла (например "000001.jpg")
    img_name = f"{img_id:06d}.jpg"   # 6 цифр с ведущими нулями
    src_path = os.path.join(images_dir, img_name)

    # создаем папку под категорию
    dst_folder = os.path.join(output_dir, str(cat_id))
    os.makedirs(dst_folder, exist_ok=True)

    # путь назначения
    dst_path = os.path.join(dst_folder, img_name)

    # копируем (или перемещаем)
    shutil.copy(src_path, dst_path)
    # если нужно переместить, используй:
    # shutil.move(src_path, dst_path)

print("✅ Изображения разложены по папкам категориям!")