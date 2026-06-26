from pathlib import Path
from collections import Counter
import numpy as np

# 클래스 분포 분석
label_dir = Path("C:/Users/tldk2/Desktop/archive/RDD_SPLIT/train/labels")

counter = Counter()

for txt_file in label_dir.glob("*.txt"):
    with open(txt_file, "r") as f:
        for line in f:
            cls = int(line.split()[0])
            counter[cls] += 1

print("Class Distribution")
print("-" * 30)

for cls, count in sorted(counter.items()):
    print(f"Class {cls}: {count}")



# 이미지 개수 확인
image_dir = Path("RDD2022/train/images")
print("Train Images:", len(list(image_dir.glob("*.*"))))


# bbox 크기 분석
widths = []
heights = []

label_dir = Path("RDD2022/train/labels")

for txt_file in label_dir.glob("*.txt"):
    with open(txt_file) as f:
        for line in f:
            parts = line.strip().split()

            w = float(parts[3])
            h = float(parts[4])

            widths.append(w)
            heights.append(h)

print("Avg Width :", sum(widths)/len(widths))
print("Avg Height:", sum(heights)/len(heights))


# bbox area 분석
areas = []

label_dir = Path("C:/Users/tldk2/Desktop/yolo11_2class/train/labels")

for txt_file in label_dir.glob("*.txt"):
    with open(txt_file) as f:
        for line in f:
            cls, x, y, w, h = map(float, line.split())

            area = w * h
            areas.append(area)

areas = np.array(areas)

print("Min Area :", areas.min())
print("Max Area :", areas.max())
print("Mean Area:", areas.mean())
print("Median   :", np.median(areas))


# invalid box 확인
invalid = []

for txt_file in Path("C:/Users/tldk2/Desktop/archive/RDD_SPLIT/train/labels").rglob("*.txt"):

    with open(txt_file) as f:
        for idx, line in enumerate(f):

            cls, x, y, w, h = map(float, line.split())

            if w <= 0 or h <= 0:
                invalid.append((txt_file, idx, line.strip()))

print("Invalid Box Count:", len(invalid))


# train/valid/test 개수 확인
print("Train:", len(list(Path("C:/Users/tldk2/Desktop/archive/RDD_SPLIT/train/images").glob("*"))))
print("Valid:", len(list(Path("C:/Users/tldk2/Desktop/archive/RDD_SPLIT/val/images").glob("*"))))
print("Test :", len(list(Path("C:/Users/tldk2/Desktop/archive/RDD_SPLIT/test/images").glob("*"))))



# remove_invalid_bbox
for txt_file in Path("RDD_SPLIT/train/labels").glob("*.txt"):

    valid_lines = []

    with open(txt_file) as f:
        for line in f:
            cls, x, y, w, h = map(float, line.split())

            if w > 0 and h > 0:
                valid_lines.append(line)

    with open(txt_file, "w") as f:
        f.writelines(valid_lines)


# make_2class_dataset
random.seed(42)

SRC_ROOT = Path("C:/Users/tldk2/Desktop/archive/RDD_SPLIT")
CLEAN_ROOT = Path("C:/Users/tldk2/Desktop/data_set")

class_map = {
    0: 0,
    1: 0,
    2: -1,
    3: -1,
    4: 1
}

for split in ["train", "valid", "test"]:

    src_img_dir = SRC_ROOT / split / "images"
    src_lbl_dir = SRC_ROOT / split / "labels"

    dst_img_dir = CLEAN_ROOT / split / "images"
    dst_lbl_dir = CLEAN_ROOT / split / "labels"

    dst_img_dir.mkdir(parents=True, exist_ok=True)
    dst_lbl_dir.mkdir(parents=True, exist_ok=True)

    for txt_path in src_lbl_dir.glob("*.txt"):

        new_lines = []

        with open(txt_path, "r") as f:
            for line in f:
                parts = line.strip().split()

                if len(parts) != 5:
                    continue

                cls = int(parts[0])
                new_cls = class_map[cls]

                if new_cls == -1:
                    continue

                parts[0] = str(new_cls)
                new_lines.append(" ".join(parts))

        if len(new_lines) == 0:
            continue

        img_path = None

        for ext in [".jpg", ".png", ".jpeg"]:
            p = src_img_dir / f"{txt_path.stem}{ext}"

            if p.exists():
                img_path = p
                break

        if img_path is None:
            continue

        shutil.copy2(img_path, dst_img_dir / img_path.name)

        with open(dst_lbl_dir / txt_path.name, "w") as f:
            f.write("\n".join(new_lines))



# Scanning
random.seed(42)

CLEAN_ROOT = Path("C:/Users/tldk2/Desktop/yolo11_2class")

for split in ["train", "valid", "test"]:

    img_dir = CLEAN_ROOT / split / "images"
    lbl_dir = CLEAN_ROOT / split / "labels"

    pothole_imgs = []
    crack_imgs = []

    for img_path in img_dir.glob("*.*"):

        txt_path = lbl_dir / f"{img_path.stem}.txt"

        if not txt_path.exists():
            continue

        has_pothole = False

        with open(txt_path, "r") as f:
            for line in f:
                cls = int(line.split()[0])

                if cls == 1:
                    has_pothole = True
                    break

        if has_pothole:
            pothole_imgs.append(img_path)
        else:
            crack_imgs.append(img_path)

    globals()[f"{split}_pothole"] = pothole_imgs
    globals()[f"{split}_crack"] = crack_imgs

# Sampling
FINAL_ROOT = Path("C:/Users/tldk2/Desktop/yolo11_2class")

TARGET = {
    "train": 5000,
    "valid": 1000,
    "test": 1000
}

POTHOLE_RATIO = 0.3

for split in ["train", "valid", "test"]:

    pothole_imgs = globals()[f"{split}_pothole"]
    crack_imgs = globals()[f"{split}_crack"]

    total = TARGET[split]

    target_pothole = min(int(total * POTHOLE_RATIO), len(pothole_imgs))
    target_crack = total - target_pothole

    target_crack = min(target_crack, len(crack_imgs))

    selected = random.sample(pothole_imgs, target_pothole) + \
               random.sample(crack_imgs, target_crack)

    random.shuffle(selected)

    out_img = FINAL_ROOT / split / "images"
    out_lbl = FINAL_ROOT / split / "labels"

    out_img.mkdir(parents=True, exist_ok=True)
    out_lbl.mkdir(parents=True, exist_ok=True)

    for img_path in selected:

        txt_path = img_path.parent.parent / "labels" / f"{img_path.stem}.txt"

        shutil.copy2(img_path, out_img / img_path.name)
        shutil.copy2(txt_path, out_lbl / txt_path.name)



# check_final_distribution
ROOT = Path("C:/Users/tldk2/Desktop/yolo11_2class")

for split in ["train","valid","test"]:

    counter = Counter()

    for txt in (ROOT/split/"labels").glob("*.txt"):

        with open(txt) as f:

            for line in f:

                cls = int(line.split()[0])

                counter[cls] += 1

    print(f"\n===== {split.upper()} =====")
    print("Crack   :", counter[0])
    print("Pothole :", counter[1])

















