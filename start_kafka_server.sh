KAFKA_HOME=~/kafka_2.12-2.3.0
export JMX_PORT=9999 && \
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties