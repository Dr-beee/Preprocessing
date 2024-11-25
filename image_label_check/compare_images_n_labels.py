import glob

root_dir = 'D:/Documents/dr_bee/dr_bee'

images_dir = f'{root_dir}/images/train'
labels_dir = f'{root_dir}/labels/train'

images = glob.glob(f'{images_dir}/*.jpg')
labels = glob.glob(f'{labels_dir}/*.txt')

# TODO : 절대경로에서 경로제거, 확장자 제거해서 파일명만 추출
images = [i.split('.')[0].split('\\')[-1] for i in images]
labels = [l.split('.')[0].split('\\')[-1] for l in labels]
print(f'[Info] len(images)={len(images)}')
print(f'[Info] len(labels)={len(labels)}')

# TODO : 리스트에서 집합으로 변환
images = set(images)
labels = set(labels)
print(f'[Info] len(images)={len(images)}')
print(f'[Info] len(labels)={len(labels)}')

data_available = images.intersection(labels)
print(f'[Info] len(data_available)={len(data_available)}')

# TODO : 
images_residual = labels.difference(images)
print(f'[Info] images_residual={images_residual}')

# Result
# [Info] len(images)=70222
# [Info] len(labels)=70225
# [Info] len(images)=70222
# [Info] len(labels)=70225
# [Info] len(data_available)=70222
# [Info] images_residual={'C_008_016_20230920180023_001_008_001_002', 'C_005_009_20230922180716_001_005_001_002', 'C_008_016_20230919100028_001_008_001_002'}