$KAFKA_HOME/bin/kafka-topics.sh --create \
  --bootstrap-server 10.0.0.10:9092 10.0.0.4:9093 10.0.0.13:9094 \
  --replication-factor 3 \
  --partitions 4 \
  --topic pageviews &
$KAFKA_HOME/bin/kafka-topics.sh --create \
  --bootstrap-server 10.0.0.10:9092 10.0.0.4:9093 10.0.0.13:9094 \
  --replication-factor 3 \
  --partitions 4 \
  --topic events &
$KAFKA_HOME/bin/kafka-topics.sh --create \
  --bootstrap-server 10.0.0.10:9092 10.0.0.4:9093 10.0.0.13:9094 \
  --replication-factor 3 \
  --partitions 4 \
  --topic display_ads