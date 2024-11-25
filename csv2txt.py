import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import shutil


df = pd.read_csv('E:/dr_bee/val.csv')

df = df.sort_values('image_id').reset_index()
print('!')

dst_dir = 'E:/dr_bee/labels/val'
for i in df.index[:]:
    filename = df['image_id'][i]

    annotation_id = df['annotation_id'][i]
    
    class_id = df['class_id'][i]
    x_center = df['x_center'][i]
    y_center = df['y_center'][i]
    w = df['width'][i]
    h = df['height'][i]

    str_output = f'{class_id} {x_center} {y_center} {w} {h}'

    # ※ 만약 파일이 없으면 생성, 만약 존재하면 추가쓰기
    with open(f"{dst_dir}/{filename}.txt", "a") as file:
        file.write(str_output + "\n")  # Write each line followed by a newline

print(':)')