checkpoint_list=("beomi/Llama-3-KoEn-8B" "beomi/OPEN-SOLAR-KO-10.7B" "beomi/gemma-ko-7b" "Qwen/Qwen2-7B")
cache_dir=/data/llmlaw/base_model
data_path=/home/seonghee_hong/legal_llm/dps/legal-project-data/CASE-LAW-sample/sampled_1000.jsonl
batch_size=2

for checkpoint in ${checkpoint_list[@]}; do
    echo "Testing $checkpoint"
    python model_test.py \
        --checkpoint $checkpoint \
        --cache_dir $cache_dir \
        --data_path $data_path \
        --batch_size $batch_size
done