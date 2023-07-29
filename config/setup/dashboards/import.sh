#!/bin/bash

import()
{
    curl -u ${ES_USER}:${ELASTIC_PASSWORD} -X POST kibana:5601/api/saved_objects/_import?overwrite=true -H "kbn-xsrf: true" --form file=@$1
}

echo "Waiting for Kibana to launch on 5601"

# for port 5601 to be avaliable
while ! curl --output /dev/null --silent --head --fail kibana:5601; do 
    sleep 1 && echo -n .; 
done;

echo "Kibana launched, might take a while to setup the service"

# give kibana service 10s to be up
sleep 10 && echo importing dashboards ...

import agents/akagents-dataview.ndjson
import agents/akagents-spec-dashboard.ndjson
import agents/akagents-info-dashboard.ndjson
import news/aknews-dataview.ndjson
import news/aknews-kibana-dashboard.ndjson