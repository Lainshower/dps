#!/bin/bash

SPARK_HOME=/opt/spark

$SPARK_HOME/bin/spark-submit \
  --master spark://222.231.24.44:7077 \
  --conf spark.executor.instances=10 \
  --conf spark.executor.cores=25 \
  --conf spark.executor.memory=64g \
  --conf spark.executor.memoryOverhead=24g \
  --conf spark.driver.memory=128g \
  --conf "spark.executor.extraJavaOptions=-XX:+UseG1GC -XX:MaxGCPauseMillis=100 -XX:InitiatingHeapOccupancyPercent=35" \
  --conf "spark.driver.extraJavaOptions=-XX:+UseG1GC -XX:MaxGCPauseMillis=100 -XX:InitiatingHeapOccupancyPercent=35" \
  --conf spark.eventLog.enabled=true \
  --conf "spark.local.dir=/data/llmlaw/tmp" \
  --conf spark.eventLog.dir=/home/kaoara/dps/eventLog \
  --conf "spark.executor.logs.rolling.strategy=time" \
  --conf "spark.executor.logs.rolling.time.interval=daily" \
  /home/kaoara/dps/bin/sparkapp.py dedup_job \
  --config_path=/home/kaoara/dps/configs/dedup_job_news.yaml \

