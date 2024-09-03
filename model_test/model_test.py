import os
import json
from tqdm import tqdm

import numpy as np
import matplotlib.pyplot as plt

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Set which GPU to use
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3,4,5,6,7"
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"


def main(args):
    def process_batch(batch):
        batch_size = len(batch)
        input_texts = [
            item['text'] if len(tokenizer.tokenize(item['text'])) <= 5000  # Redundant
            else tokenizer.decode(tokenizer.encode(item['text'], truncation=True, max_length=5100), skip_special_tokens=True)
            for item in batch
        ]

        # Tokenize inputs with padding and truncation
        input_ids = tokenizer(input_texts, return_tensors="pt", padding=True, truncation=True).input_ids
        input_ids = input_ids.to(model.device)

        # Calculate loss for each sample individually
        with torch.no_grad():
            outputs = model(input_ids=input_ids, labels=input_ids)
            logits = outputs.logits

            # Initialize a list to store PPL for each sample
            ppl_list = []

            # Iterate through each sample in the batch
            for i in range(batch_size):
                # Compute loss for the individual sample
                shift_logits = logits[i, :-1, :].contiguous()
                shift_labels = input_ids[i, 1:].contiguous()

                loss_fct = torch.nn.CrossEntropyLoss(reduction='sum', ignore_index=tokenizer.pad_token_id)
                individual_loss = loss_fct(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1))

                # Calculate PPL for the individual sample
                non_pad_tokens = (shift_labels != tokenizer.pad_token_id).sum()
                ppl = torch.exp(individual_loss / non_pad_tokens)
                ppl_list.append(ppl.item())

        # Record results
        for i, item in enumerate(batch):
            results.append({
                'text': item['text'],
                'input': input_texts[i],
                'ppl': ppl_list[i]
            })


    # Set tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(args.checkpoint)
    model = AutoModelForCausalLM.from_pretrained(args.checkpoint, device_map='auto', cache_dir=args.cache_dir)

    # Set tokenizer padding token to eos token (Not Accurate but Temporary)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Load Data
    with open(args.data_path, 'r', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]

    # Calculate Perplexity (PPL)
    results = []

    for i in tqdm(range(0, len(data), args.batch_size)):
        batch = data[i:i+args.batch_size]
        process_batch(batch)

    # Save results
    output_path = f"{args.checkpoint.split('/')[-1]}_ppl_sampled_1000.jsonl"
    with open(output_path, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')

    # Draw Boxplot and save
    ppl = [item['ppl'] for item in results]

    max_ppl = max(ppl)
    min_ppl = min(ppl)
    median_ppl = np.median(ppl)

    plt.boxplot(ppl)
    plt.title(f"Perplexity Distribution of {args.checkpoint.split('/')[-1]}")
    plt.xlabel(f'Max: {max_ppl:.2f}, Min: {min_ppl:.2f}, Median: {median_ppl:.2f}')
    plt.ylabel('Perplexity (PPL)')
    plt.text(1.2, max_ppl, f'Max: {max_ppl:.2f}', fontsize=11, ha='center', va='bottom')
    plt.text(1.2, min_ppl, f'Min: {min_ppl:.2f}', fontsize=11, ha='center', va='bottom')
    plt.text(1.2, median_ppl, f'Median: {median_ppl:.2f}', fontsize=11, ha='center', va='bottom')
    plt.savefig(f"{args.checkpoint.split('/')[-1]}_ppl_sampled_1000_result.png")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint', type=str, required=True, help='Model Name or Path (e.g., beomi/Llama-3-KoEn-8B)')
    parser.add_argument('--cache_dir', type=str, default='/data/llmlaw/base_model', help='Path to the model cache directory')
    parser.add_argument('--data_path', type=str, default='/home/seonghee_hong/legal_llm/dps/legal-project-data/CASE-LAW-sample/sampled_1000.jsonl', required=True, help='Path to the data')
    parser.add_argument('--batch_size', type=int, default=8, help='Batch size for calculating PPL')

    args = parser.parse_args()
    main(args)