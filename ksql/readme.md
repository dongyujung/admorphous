# KSQL Node  

## Installations    

Environment: Linux  

Install as root user.  
  
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

## Calculation 1: windowed aggregation of pageviews  

Count the number of views of each webpage during a window of ten minutes.  

```sql

```  