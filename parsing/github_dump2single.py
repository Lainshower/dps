import glob
import json
import argparse

def merge_text_fields(base_path):
    # 모든 .jsonl 파일 경로 찾기
    file_paths = glob.glob(f"{base_path}/*.jsonl", recursive=True)
    file_paths = file_paths[:3] # We Just Use 4 Of Code Files.
    output_path = f"{base_path}/all-code.jsonl"
    # output_path = "/home/kaoara/data/General/github-data/all-code.jsonl"

    # 최종 파일에 'text' 필드를 저장합니다.
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for file_path in file_paths:
            with open(file_path, 'r', encoding='utf-8') as infile:
                for line in infile:
                    # 각 줄을 JSON 객체로 파싱
                    json_object = json.loads(line)
                    # 'text' 필드가 있는지 확인 후 저장
                    if 'text' in json_object:
                        json_string = json.dumps({"text": json_object['text']}, ensure_ascii=False)
                        outfile.write(json_string + '\n')

    print(f"All 'text' fields have been merged into {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge 'text' fields from JSONL files into one file.")
    parser.add_argument('--base_path', type=str, default='/data/llmlaw/General/github-data', help='Base directory path where JSONL files are stored')
    args = parser.parse_args()

    merge_text_fields(args.base_path)
