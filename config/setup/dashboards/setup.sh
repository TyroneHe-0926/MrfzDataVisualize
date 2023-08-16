#!/usr/bin/env bash

source ./lib.sh

import()
{
    curl -u ${ES_USER}:${ELASTIC_PASSWORD} -X POST kibana:5601/api/saved_objects/_import?overwrite=true -H "kbn-xsrf: true" --form file=@$1
}

log 'Waiting for availability of Elasticsearch. This can take several minutes.'

declare -i exit_code=0
wait_for_elasticsearch || exit_code=$?

if ((exit_code)); then
	case $exit_code in
		6)
			suberr 'Could not resolve host. Is Elasticsearch running?'
			;;
		7)
			suberr 'Failed to connect to host. Is Elasticsearch healthy?'
			;;
		28)
			suberr 'Timeout connecting to host. Is Elasticsearch healthy?'
			;;
		*)
			suberr "Connection to Elasticsearch failed. Exit code: ${exit_code}"
			;;
	esac

	exit $exit_code
fi

sublog 'Elasticsearch is running'

set_user_password "kibana_system" "${KIBANA_SYSTEM_PASSWORD}"

echo "Waiting for Kibana to launch on 5601"

# for port 5601 to be avaliable
while ! curl --output /dev/null --silent --head --fail kibana:5601; do 
    sleep 1 && echo -n .; 
done;

echo "Kibana launched, might take a while to setup the service"

# give kibana service 10s to be up
sleep 20 && echo importing dashboards ...

import agents/akagents-dataview.ndjson
import agents/akagents-spec-dashboard.ndjson
import agents/akagents-info-dashboard.ndjson
import news/aknews-dataview.ndjson
import news/aknews-kibana-dashboard.ndjson