#!/bin/bash

ES_USER=$1
ES_PASSWORD=$2

echo "Waiting for Kibana to launch on 5601"

while ! curl --output /dev/null --silent --head --fail kibana:5601; do 
    sleep 1 && echo -n .; 
done;

echo "Kibana launched"

curl -u ES_USER:ES_PASSWORD -X POST localhost:5601/api/saved_objects/_import?overwrite=true -H "kbn-xsrf: true" --form file=@agents/akagents-dataview.ndjson

curl -u ES_USER:ES_PASSWORD -X POST localhost:5601/api/saved_objects/_import?overwrite=true -H "kbn-xsrf: true" --form file=@agents/akagents-spec-dashboard.ndjson

curl -u ES_USER:ES_PASSWORD -X POST localhost:5601/api/saved_objects/_import?overwrite=true -H "kbn-xsrf: true" --form file=@agents/akagents-info-dashboard.ndjson