# KSQL Node  

Stream processing with KSQL.  

The messages in the three different topics are read into streams in KSQL and 
processed. The processed streams are sent into two different topics in the 
Kafka cluster.  

## Processes  

### Process 1  
  
`views_page.sql` Pageviews / Article / Window of time (windowed aggregation)  

### Process 2    

`impressions_ad.sql` Impressions / Ad (aggregation)    

## Operation  

To initiate all processes, run  

```shell script
sh ~/admorphous/process_streams.sh
```

## Setup  

OS: Linux    

Install as root user:  

  
- Java8  

```shell script
sudo apt install openjdk-8-jdk
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$PATH:$JAVA_HOME/bin
```
- KSQL from Confluent  

```shell script
wget -qO - https://packages.confluent.io/deb/5.3/archive.key | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://packages.confluent.io/deb/5.3 stable main"
```

- git  
