PRODUCERS_HOME=~/admorphous/producers/scripts
python3 $PRODUCERS_HOME/pageview_to_topic.py 1 localhost:9092 &
python3 $PRODUCERS_HOME/event_to_topic.py 1 10 localhost:9092