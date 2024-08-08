import sys
import os
from pyspark.sql import SparkSession

def merge_json_parts(source_dir, output_file):
    with open(output_file, 'w') as outfile:
        for filename in sorted(os.listdir(source_dir)):
            if filename.startswith('part') and filename.endswith('.json'):
                file_path = os.path.join(source_dir, filename)
                with open(file_path, 'r') as read_file:
                    for line in read_file:
                        outfile.write(line)

def convert_and_merge_jsonl(directory_path, temp_dir, final_filename):
    spark = SparkSession.builder.appName("Convert and Merge JSONL") \
        .config("spark.executor.memory", "16g") \
        .config("spark.executor.cores", "4") \
        .getOrCreate()

    part_file_path = f"{directory_path}/part-00000"
    df = spark.read.json(part_file_path)

    temp_output_path = f"{temp_dir}/temp_jsonl_output"
    df.repartition(4).write.mode("overwrite").json(temp_output_path)

    final_output_path = f"{directory_path}/{final_filename}.jsonl"
    merge_json_parts(temp_output_path, final_output_path)

    os.system(f"rm -r {temp_output_path}")

    spark.stop()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <directory_path> <temp_dir> <final_filename>")
        sys.exit(1)
    
    directory_path = sys.argv[1]
    temp_dir = sys.argv[2]
    final_filename = sys.argv[3]
    convert_and_merge_jsonl(directory_path, temp_dir, final_filename)
