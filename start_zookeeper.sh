KAFKA_HOME=~/kafka_2.12-2.3.0
export JMX_PORT=9999 && \
nohup $KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties