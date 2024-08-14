import argparse
import os

def split_jsonl_file(input_file, lines_per_file):
    base_dir = os.path.dirname(input_file)
    output_dir = f"{base_dir}-split" 

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r', encoding='utf-8') as file:
        file_count = 1
        current_file = open(os.path.join(output_dir, f'split_{file_count}.jsonl'), 'w', encoding='utf-8')
        for i, line in enumerate(file):
            if i > 0 and i % lines_per_file == 0:
                current_file.close()
                file_count += 1
                current_file = open(os.path.join(output_dir, f'split_{file_count}.jsonl'), 'w', encoding='utf-8')
            current_file.write(line)
        current_file.close()

    print(f"Done! Split the file into {file_count} parts.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a large JSONL file into smaller parts.")
    parser.add_argument("input_file", type=str, help="The path to the JSONL file to split.")
    parser.add_argument("--lines_per_file", type=int, default=1000, help="Number of lines per output file.")

    args = parser.parse_args()

    split_jsonl_file(args.input_file, args.lines_per_file)
