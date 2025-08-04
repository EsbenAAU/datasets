import os
import sys
import json
import numpy as np
from collections import defaultdict

def count_coco_categories(folder_path):
    category_totals = defaultdict(int)
    category_id_to_name = {}

    found_files = 0
    processed_files = 0

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            found_files += 1
            filepath = os.path.join(folder_path, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    # Tjek om det er COCO-format
                    if "annotations" in data and "categories" in data:
                        processed_files += 1

                        for cat in data["categories"]:
                            category_id_to_name[cat["id"]] = cat["name"]

                        for ann in data["annotations"]:
                            cat_id = ann.get("category_id")
                            if cat_id is not None:
                                category_totals[cat_id] += 1
                    else:
                        print(f"⚠️  Ikke COCO-format: {filename}")
            except Exception as e:
                print(f"Fejl ved {filename}: {e}")

    print(f"\n🔍 Fandt {found_files} .json-filer, behandlede {processed_files} som COCO.")

    if not category_totals:
        print("❌ Ingen kategorier fundet.")
        return {}

    # Konverter og sortér
    result = {
        category_id_to_name.get(cid, f"unknown_{cid}"): count
        for cid, count in category_totals.items()
    }
    result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))

    print("\n📊 Resultat:")
    names_array = np.array(list(result.keys()))
    count_array = np.array(list(result.values()))

    names_string = ', '.join(map(str, names_array))
    count_string = ', '.join(map(str, count_array))

    print(names_string)
    print(count_string)

    return result


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Brug: python extract.py <sti_til_mappe>")
        sys.exit(1)

    folder = sys.argv[1]
    if not os.path.isdir(folder):
        print(f"❌ Mappen findes ikke: {folder}")
        sys.exit(1)

    count_coco_categories(folder)
