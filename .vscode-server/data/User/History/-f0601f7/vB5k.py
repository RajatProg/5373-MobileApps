from mongoManager import MongoManager
import json
import glob
import os
from PIL import Image
import io

def convert_jpg_to_png_in_memory(jpg_path):
    try:
        with Image.open(jpg_path) as img:
            in_memory_file = io.BytesIO()
            img.save(in_memory_file, format='PNG')
            in_memory_file.seek(0)
            return in_memory_file.getvalue()
    except IOError as e:
        print(f"Error converting image {jpg_path}: {e}")
        return None

def load():
    json_files = glob.glob(os.path.join(".", "categoryJson", "*.json"))

    db = MongoManager()
    db.setDb("candy_store_2")
    db.dropCollection('candies')
    db.dropCollection('categories')
    db.dropCollection('images')

    category_id = 0
    candy_long_ids = []
    big_candy_dict = {}

    for file in json_files:
        print(file)
        parts = os.path.split(file)
        image_folder = parts[-1][:-5]
        category = image_folder.replace("-", " ").title()

        print(category)

        with open(file) as f:
            data = json.load(f)
            summary = {"count": len(data), "name": category, "_id": category_id, "candies": []}
            category_id += 1

            for id, item in data.items():
                item.setdefault("categories", [])
                
                if id not in candy_long_ids:
                    candy_long_ids.append(id)
                    index = candy_long_ids.index(id)
                    item["_id"] = index
                    big_candy_dict[index] = item
                    summary["candies"].append(index)
                    item['img_path'] = os.path.join(".", "images", image_folder, id + '.jpg')
                else:
                    index = candy_long_ids.index(id)
                    print(f"id: {id} exists at {index}! " + "="*20)
                
                big_candy_dict[index]["categories"].append(category_id)

            db.setCollection('categories')
            db.post(summary)

    db.setCollection("candies")
    for id, item in big_candy_dict.items():
        db.post(item)

    db.setCollection("images")
    for id, item in big_candy_dict.items():
        png_data = convert_jpg_to_png_in_memory(item['img_path'])
        if png_data:
            db.store_image_in_mongodb(id, png_data)

    print(len(big_candy_dict))
    with open("big_updated_candy.json", "w") as f:
        json.dump(big_candy_dict, f)

if __name__ == "__main__":
    load()
