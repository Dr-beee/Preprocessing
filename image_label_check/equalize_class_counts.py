import os
import random

# 폴더 경로 설정
images_path = './images'
labels_path = './labels'

# 서브 폴더 경로 설정
images_train_path = os.path.join(images_path, 'train')
images_val_path = os.path.join(images_path, 'val')
labels_train_path = os.path.join(labels_path, 'train')
labels_val_path = os.path.join(labels_path, 'val')

# 접두사별 파일 그룹 분리 함수
def group_files_by_prefix(path):
    files = os.listdir(path)
    grouped_files = {'A': [], 'B': [], 'C': []}
    for file in files:
        if file.startswith('A'):
            grouped_files['A'].append(file)
        elif file.startswith('B'):
            grouped_files['B'].append(file)
        elif file.startswith('C'):
            grouped_files['C'].append(file)
    return grouped_files

# 파일 그룹 동기화 및 제거 함수
def synchronize_and_remove(files_group, images_dir, labels_dir, prefix, target_count):
    files_to_remove = len(files_group[prefix]) - target_count
    if files_to_remove > 0:
        files_to_remove_list = random.sample(files_group[prefix], files_to_remove)
        for file in files_to_remove_list:
            # 이미지와 라벨 파일 경로
            image_file_path = os.path.join(images_dir, file)
            label_file_path = os.path.join(labels_dir, file.replace('.jpg', '.txt'))

            # 이미지와 라벨 파일 삭제
            if os.path.exists(image_file_path):
                os.remove(image_file_path)
            if os.path.exists(label_file_path):
                os.remove(label_file_path)

# 메인 함수
def main():
    # 학습(train) 데이터셋과 검증(val) 데이터셋 처리
    for images_dir, labels_dir in [(images_train_path, labels_train_path), (images_val_path, labels_val_path)]:
        # 접두사별 파일 그룹 분리
        images_group = group_files_by_prefix(images_dir)
        labels_group = group_files_by_prefix(labels_dir)

        # 파일 그룹의 개수 일치 여부 확인 및 로깅
        for prefix in ['A', 'B', 'C']:
            if len(images_group[prefix]) != len(labels_group[prefix]):
                print(f"[경고] {prefix}로 시작하는 이미지와 라벨 파일의 개수가 일치하지 않습니다.")
        print('[제거 전] 모든 파일들의 개수가 동일해요')
      
        # B 접두사의 파일 개수 가져오기
        target_count = len(images_group['B'])

        # A와 C 접두사의 파일 개수를 B의 개수에 맞춰서 동기화
        for prefix in ['A', 'C']:
            synchronize_and_remove(images_group, images_dir, labels_dir, prefix, target_count)
        
        images_group = group_files_by_prefix(images_dir)
        labels_group = group_files_by_prefix(labels_dir)

        # 파일 그룹의 개수 일치 여부 확인 및 로깅
        for prefix in ['A', 'B', 'C']:
            if len(images_group[prefix]) != len(labels_group[prefix]):
                print(f"[경고] {prefix}로 시작하는 이미지와 라벨 파일의 개수가 일치하지 않습니다.")
        print('[제거 후] 모든 파일들의 개수가 동일해요')

if __name__ == "__main__":
    main()
