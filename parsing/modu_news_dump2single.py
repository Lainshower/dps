import argparse
import glob
import json

def merge_jsonl_files(year):
    # Base path 설정을 정확하게 해주세요.
    base_path = '/home/kaoara/data/General/'
    # 파일들이 있는 정확한 디렉토리 경로 패턴을 설정합니다.
    pattern = f"{base_path}/MODU_NEWSPAPER_{year}_v1.0-filtered-json/*.jsonl"
    # 최종 파일 저장 경로 설정 (.json이 아니라 .jsonl로 변경)
    output_path = f"{base_path}/MODU_NEWSPAPER_{year}_v1.0-filtered-json/{year}-articles.jsonl"

    # 일치하는 모든 파일 경로를 찾습니다.
    file_paths = glob.glob(pattern)

    # 최종 파일에 모든 내용을 저장합니다.
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for file_path in file_paths:
            with open(file_path, 'r', encoding='utf-8') as infile:
                for line in infile:
                    # 각 줄을 그대로 복사하여 저장합니다.
                    outfile.write(line)

    print(f"All JSONL files for {year} have been merged into {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Merge JSONL files based on year.')
    # --year 플래그를 사용하여 연도를 입력받습니다.
    parser.add_argument('--year', type=str, required=True, help='Year to filter and merge JSONL files')
    args = parser.parse_args()

    merge_jsonl_files(args.year)
