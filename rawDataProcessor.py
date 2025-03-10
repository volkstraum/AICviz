import json
import csv
import os

path = "artworks"
outputname = "datasets/artworks.csv"

datalist = []



with open(f"{path}/9.json") as file:
    data = json.load(file)

dicfield = []

for everykey in data:
    dicfield.append(everykey)

fields_to_keep = [
    "id","title","date_start","date_end","date_display","artist_display","place_of_origin",
    "description","dimensions","medium_display","inscriptions","is_on_view","gallery_title",
    "artwork_type_title","department_title","artist_id","artist_title","artist_ids",
    "artist_titles","category_titles","style_title","style_titles","classification_title",
    "classification_titles","subject_titles","material_titles","technique_titles","theme_titles"
]

with open(outputname, "w", newline="", encoding="utf-8") as csvfile:
    writer=csv.writer(csvfile)
    writer.writerow(fields_to_keep)
    for filename in os.listdir(path):
        if filename.endswith(".json"):
            with open(os.path.join(path, filename), "r", encoding="utf-8") as file:
                data = json.load(file)
                row = [data.get(key, "N/A") for key in fields_to_keep]
                writer.writerow(row)

print(f"CSV file '{outputname}' be out here dawg.")

