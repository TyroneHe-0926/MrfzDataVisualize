ARG ELASTIC_VERSION
ARG ELASTIC_PASSWORD

# https://www.docker.elastic.co/
FROM docker.elastic.co/kibana/kibana:${ELASTIC_VERSION}
COPY ./dashboards /dashboards
WORKDIR /dashboards

# import dashboards
# ENTRYPOINT [ "sh", "import.sh" ]
