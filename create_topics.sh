$KAFKA_HOME/bin/kafka-topics.sh --create \
  --bootstrap-server 10.0.0.10:9092 10.0.0.4:9092 10.0.0.13:9092 \
  --replication-factor 2 \
  --partitions 4 \
  --topic pageviews &
$KAFKA_HOME/bin/kafka-topics.sh --create \
  --bootstrap-server 10.0.0.10:9092 10.0.0.4:9092 10.0.0.13:9092 \
  --replication-factor 2 \
  --partitions 4 \
  --topic events &
$KAFKA_HOME/bin/kafka-topics.sh --create \
  --bootstrap-server 10.0.0.10:9092 10.0.0.4:9092 10.0.0.13:9092 \
  --replication-factor 2 \
  --partitions 4 \
  --topic display_ad