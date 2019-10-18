
PRODUCERS_HOME=~/admorphous/producers/scripts
python3 $PRODUCERS_HOME/pageview_to_topic.py 0.01 10.0.0.10:9092 10.0.0.4:9093 10.0.0.13:9094 &
python3 $PRODUCERS_HOME/event_to_topic.py 0.01 100 10.0.0.10:9092 10.0.0.4:9093 10.0.0.13:9094