import os
import random
import argparse

def sample_jsonl(directory, sample_size=20000):
    jsonl_path = os.path.join(directory, 'preprocessed.jsonl')
    sampled_path = os.path.join(directory, 'sampled.jsonl')
    
    if not os.path.isfile(jsonl_path):
        raise FileNotFoundError(f"{jsonl_path} 파일을 찾을 수 없습니다.")
    
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    sampled_lines = random.sample(lines, min(sample_size, len(lines)))
    
    with open(sampled_path, 'w', encoding='utf-8') as f:
        for line in sampled_lines:
            f.write(line)
    
    print(f"{len(sampled_lines)}개의 샘플링된 데이터가 {sampled_path}에 저장되었습니다.")

# 메인 함수
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="deduplication.jsonl에서 데이터를 샘플링합니다.")
    parser.add_argument('directory', type=str, help="deduplication.jsonl 파일이 있는 디렉토리 경로")
    parser.add_argument('--sample_size', type=int, default=20000, help="샘플링할 데이터의 수 (기본값: 20000)")
    
    args = parser.parse_args()
    
    # 샘플링 수행
    sample_jsonl(args.directory, args.sample_size)
