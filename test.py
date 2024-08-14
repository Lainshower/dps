from pyspark.sql import SparkSession

def read_line(line):
    """한 줄의 JSON 데이터를 파싱하는 함수."""
    import json
    try:
        data = json.loads(line)
        return data
    except json.JSONDecodeError:
        return None

def main():
    # 스파크 세션 생성
    spark = SparkSession.builder \
        .appName("Filter Test") \
        .master("local[*]") \
        .config("spark.executor.memory", "16g") \
        .config("spark.driver.memory", "16g") \
        .config("spark.executor.memoryOverhead", "4g") \
        .getOrCreate()

    sc = spark.sparkContext

    # 파일 경로 설정
    file_path = "/home/kaoara/dps/legal-project-data/General_First_Dedup_WIKI/deduplication.jsonl"

    # 데이터 읽기
    data_rdd = sc.textFile(file_path)
    parsed_rdd = data_rdd.map(read_line).filter(lambda x: x is not None)

    # text 필드의 길이를 계산
    length_rdd = parsed_rdd.map(lambda x: len(x.get('text', '\n').split()))

    # 최소값과 최대값 계산
    min_length = length_rdd.min()
    max_length = length_rdd.max()

    print(f"Minimum text length: {min_length}")
    print(f"Maximum text length: {max_length}")

    # 세션 종료
    spark.stop()

if __name__ == "__main__":
    main()
