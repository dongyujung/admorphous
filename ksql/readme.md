# KSQL Node  

Stream processing with KSQL.  

## Processes  

### Process 1  
  
`views_page.sql` Pageviews / Article / Window of time (windowed aggregation)  

### Process 2    

`impressions_ad.sql` Impressions / Ad (aggregation)    

## Operation  

To initiate all processes, run  

```bash
sh ~/admorphous/process_streams.sh
```

## Setup  

OS: Linux    

Install as root user:  

  
- Java8  

```bash
sudo apt install openjdk-8-jdk
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$PATH:$JAVA_HOME/bin
```
- KSQL from Confluent  

```bash
wget -qO - https://packages.confluent.io/deb/5.3/archive.key | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://packages.confluent.io/deb/5.3 stable main"
```

