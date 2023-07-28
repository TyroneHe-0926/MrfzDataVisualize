ARG ES_USER
ARG ELASTIC_PASSWORD

FROM ubuntu

ENV ES_USER_ENV=$ES_USER
ENV ES_PASS_ENV=$ELASTIC_PASSWORD

COPY ./dashboards /dashboards
WORKDIR /dashboards

RUN apt update
RUN apt install -y curl

# import dashboards
ENTRYPOINT sh ./import.sh $ES_USER_ENV, $ES_PASS_ENV
