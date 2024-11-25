import os
import json
import pandas as pd
import csv
import logging

logging.basicConfig(
    filename="label_data_error.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# [JSON 파일을 담은 폴더]와 같은 위치에서 프로그램 실행
root_folder = "./"
output_csv = "label_data.csv"
output_text_folder="Label_data_text"
header = [
    "image_id",
    "annotation_id",
    "class_id",
    "x_center",
    "y_center",
    "width",
    "height",
    "disease",
]


if not os.path.exists(output_csv):
    with open(output_csv, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(header)
if not os.path.exists(output_text_folder):
    os.makedirs(output_text_folder)

folders=os.walk(root_folder)
for root, dirs, files in folders:
    for file in files:
        if file.endswith(".json"):
            json_path = os.path.join(root, file)
            folder_name = int(os.path.basename(root))
            image_id = str(os.path.splitext(file)[0])
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    label_data = json.load(f)
            except:
                logging.error(f"[{folder_name}-{image_id}]이미지 저장 실패 - file 읽기부터 실패")
                print(f"[{folder_name}-{image_id}]이미지 저장 실패 - file 읽기부터 실패")
                continue

            image_all_data = []
            cateogory = label_data["categories"]
            image_width = float(label_data["image"]["width"]) #1920
            image_height = float(label_data["image"]["height"]) #1080
            
            larva_count = 0
            for data in label_data["annotations"]:

                annotation_id = int(data["id"])
                class_id = int(data["category_id"]) - 4  # [0,2]의 class

                if class_id < 0:
                    larva_count += 1

                min_x, min_y, max_x, max_y = map(float, data["bbox"])
                x_center, y_center = (min_x + max_x) / (6*640), (min_y + max_y) / (6*640)+7/32
                width, height = (max_x - min_x) / image_width, (max_y - min_y) / image_width
                disease = cateogory[int(data["category_id"])]["name"].split("_")[1]

                image_all_data.append(
                    [
                        image_id,
                        annotation_id,
                        class_id,
                        x_center,
                        y_center,
                        width,
                        height,
                        disease,
                    ]
                )

            if larva_count == len(image_all_data):  # 성충 없이 유충만 있는 data log에 기록
                logging.warning(f"[{folder_name}-{image_id}]에 유충 데이터만 있음")
                print(f"[{folder_name}-{image_id}]에 유충 데이터만 있음")
            if len(image_all_data) == len(label_data["annotations"]):
                try:
                    with open(output_csv, mode="a", newline="", encoding="utf-8-sig") as f:
                        writer = csv.writer(f)
                        writer.writerows(image_all_data)
                except:
                    logging.error(f"[{folder_name}-{image_id}]이미지 저장 실패 - file에 저장을 못함" )
                    print(f"[{folder_name}-{image_id}]이미지 저장 실패 - file에 저장을 못함")
            else:
                logging.error(f"[{folder_name}-{image_id}]이미지 저장 실패 - row를 저장하지 못함")
                print(f"[{folder_name}-{image_id}]이미지 저장 실패 - row를 저장하지 못함")

# pandas를 이용해서 csv 재편집
# 중복 데이터 제거
# 유충 데이터(class_id<0) 제거
if os.path.exists(output_csv):
    print("--csv 중복 제거, 유충 데이터 제거 실행--")
    df = pd.read_csv(output_csv)
    # id가 중복되는 데이터 제거
    duplicates = df[df.duplicated(subset=["image_id", "annotation_id"], keep=False)]
    unique_duplicates = duplicates.groupby(["image_id", "annotation_id"]).first().reset_index()
    if not unique_duplicates.empty:
        logging.info("----중복 데이터 발견 및 제거된 항목----")
        for row in duplicates.itertuples(index=False):
            logging.warning(f"image_id={row.image_id}, annotation_id={row.annotation_id}가 겹칩니다")
            print(f"image_id={row.image_id}, annotation_id={row.annotation_id}가 겹칩니다")
        logging.info("----------------------------------------")
    df = df.drop_duplicates(subset=["image_id", "annotation_id"])

    # 같은 id에서 완전 동일한 데이터 제거
    df = df.drop_duplicates(subset=["image_id", "class_id", "x_center", "y_center", "width", "height", "disease"])
    
    # 유충 데이터 제거
    df = df[df["class_id"] >= 0]
    df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    
    for row in df.itertuples(index=False):
        try:
            output_text = f"{row.image_id}.txt"
            output_text_path = os.path.join(output_text_folder, output_text)
            with open(output_text_path, mode="a", encoding="utf-8") as f:
                f.write(f"{str(row.class_id)} {row.x_center} {row.y_center} {row.width} {row.height}\n")
        except:
            logging.error(f"[{row.image_id}].txt 저장 오류")
else:
    print("csv의 pandas 작업 실패")
