#!/bin/bash

# 원본 및 대상 디렉토리 설정
base_dir='/data/llmlaw/RAW-DATA/Domain'
dest_dir='/home/kaoara/dps/legal-project-data/Domain-Book'

# 파일 및 디렉토리 복사
cp -r "$base_dir/Aihub/aihub_expert_corpus_book.jsonl" "$dest_dir"
cp -r "$base_dir/Textbook/2017_administrative_law.jsonl" "$dest_dir"
cp -r "$base_dir/Textbook/2017_provisions_of_civil_law.jsonl" "$dest_dir"
cp -r "$base_dir/Textbook/basic_of_civil_law.jsonl" "$dest_dir"
cp -r "$base_dir/Textbook/civil_law_case_study.jsonl" "$dest_dir"
cp -r "$base_dir/Textbook/criminal_law_case_study.jsonl" "$dest_dir"
cp -r "$base_dir/Textbook/criminal_law.jsonl" "$dest_dir"
cp -r "$base_dir/Textbook/criminal_law_overview.jsonl" "$dest_dir"
cp -r "$base_dir/Textbook/legal_ethics_2023.jsonl" "$dest_dir"
cp -r "$base_dir/Textbook/urban_planning_case_law.jsonl" "$dest_dir"
cp -r "$base_dir/Textbook/patent_case_law.jsonl" "$dest_dir"
cp -r "$base_dir/Textbook/easylaw.jsonl" "$dest_dir"