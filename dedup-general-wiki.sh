#!/bin/bash

SPARK_HOME=/opt/spark

$SPARK_HOME/bin/spark-submit \
  --master spark://222.231.24.44:7077 \
  --conf spark.executor.instances=32 \
  --conf spark.executor.cores=8 \
  --conf spark.executor.memory=24g \
  --conf spark.executor.memoryOverhead=4g \
  --conf spark.driver.memory=48g \
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
  --conf spark.shuffle.file.buffer=64k \
  --conf spark.reducer.maxSizeInFlight=48m \
  --conf spark.locality.wait=3s \
  /home/kaoara/dps/bin/sparkapp.py dedup_job \
  --config_path=/home/kaoara/dps/configs/dedup_job_wiki.yaml
