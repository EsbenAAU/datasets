import os
import numpy as np
from collections import defaultdict

def count_yolo_classes(yolo_folder):
    class_counts = defaultdict(int)

    for filename in os.listdir(yolo_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(yolo_folder, filename)
            with open(filepath, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        class_id = int(line.split()[0])
                        class_counts[class_id] += 1

    # Sorter efter antal
    sorted_items = sorted(class_counts.items(), key=lambda x: x[1], reverse=True)

    class_ids = np.array([item[0] for item in sorted_items])
    counts = np.array([item[1] for item in sorted_items])

    print("class_ids =", class_ids)
    print("counts    =", counts)

    return class_ids, counts


# Eksempel på brug:
if __name__ == "__main__":
    folder = "/sti/til/dine/yolo/annotations"  # fx "/home/ubuntu/yolo/labels"
    count_yolo_classes(folder)
