export JMX_PORT=9999 && \
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 && \
KSQL_OPTS="-Dksql.streams.num.streams.threads=4" && \
/usr/bin/ksql-server-start /etc/ksql/ksql-server.properties