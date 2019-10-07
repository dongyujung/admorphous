# AdMorphous: Ingestion and Stream Processing Integration with Kafka

In this project, I have utilized an API-style stream processing
framework on top of Kafka, integrating both ingestion and stream 
processing into a single framework.  
The purpose is to build a reactive and scalable pipeline for advertisements.  
The data used is the ["Outbrain Click Prediction"](https://www.kaggle.com/c/outbrain-click-prediction/data) data from Kaggle.  

![alt text](./images/data.png "data")  

## System Overview  

![alt text](./images/system.png "system")  

The system removes the sequential stream processing step after the ingestion, and integrates it into the Kafka framework.  
The following image depicts the pros and cons of using Kafka streams for this purpose.    

![alt text](./images/structure5.png "structure")  

The repository is organized so that files of each part of the system are in each directory. The parts are:  

- Producers  
- Kafka Cluster  
- KSQL  
- DB  
- Dashboard  



