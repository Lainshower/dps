#!/bin/bash

SPARK_HOME=/opt/spark

$SPARK_HOME/bin/spark-submit \
  --master spark://222.231.24.44:7077 \
  --conf spark.executor.instances=100 \
  --conf spark.executor.cores=10 \
  --conf spark.executor.memory=120g \
  --conf spark.executor.memoryOverhead=8g \
  --conf spark.driver.memory=64g \
  --conf "spark.executor.extraJavaOptions=-XX:+UseG1GC -XX:MaxGCPauseMillis=200 -XX:InitiatingHeapOccupancyPercent=35" \
  --conf "spark.driver.extraJavaOptions=-XX:+UseG1GC -XX:MaxGCPauseMillis=200 -XX:InitiatingHeapOccupancyPercent=35" \
  --conf spark.eventLog.enabled=true \
  --conf "spark.local.dir=/data/llmlaw/tmp" \
  --conf spark.eventLog.dir=/home/kaoara/dps/eventLog \
  --conf "spark.executor.logs.rolling.strategy=time" \
  --conf "spark.executor.logs.rolling.time.interval=daily" \
  --conf spark.network.timeout=800s \
  --conf spark.executor.heartbeatInterval=120s \
  --conf spark.shuffle.service.enabled=true \
  --conf spark.sql.shuffle.partitions=1000 \
  --conf spark.shuffle.compress=true \
  --conf spark.shuffle.file.buffer=128k \
  --conf spark.reducer.maxSizeInFlight=96m \
  --conf spark.locality.wait=10s \
  --conf spark.memory.fraction=0.6 \
  --conf spark.memory.storageFraction=0.4 \
  /home/kaoara/dps/bin/sparkapp.py dedup_job \
  --config_path=/home/kaoara/dps/configs/dedup_job_news.yaml \

