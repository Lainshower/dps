import glob
import json

# articles.jsonl 파일들이 위치한 디렉토리 경로를 설정합니다.
base_path = '/home/kaoara/data/General/AIHUB-NEWS-filtered-json'  # 여기에 실제 경로를 입력해주세요.

# 통합 파일 생성 경로
output_file_path = f'{base_path}/all-articles.jsonl'

# 모든 article.jsonl 파일 경로 찾기
file_paths = glob.glob(f'{base_path}/*.jsonl', recursive=True)

# 통합 파일 생성
with open(output_file_path, 'w', encoding='utf-8') as outfile:
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as infile:
            for line in infile:
                # 각 줄을 JSON 객체로 읽어서 다시 JSON 문자열로 변환 후 저장
                json_object = json.loads(line)
                json_string = json.dumps(json_object, ensure_ascii=False)
                outfile.write(json_string + '\n')

print(f'모든 파일이 {output_file_path}로 성공적으로 병합되었습니다.')