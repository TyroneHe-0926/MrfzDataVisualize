FROM ubuntu

COPY ./dashboards /dashboards
WORKDIR /dashboards

RUN apt update
RUN apt install -y curl

# import dashboards
ENTRYPOINT bash ./setup.sh
