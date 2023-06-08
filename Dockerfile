FROM ubuntu:latest
MAINTAINER Michael Schwarz

COPY server.py requirements.txt /opt/
WORKDIR /opt

RUN apt-get update && \
    apt-get install -y python3 python3-pip 

ENTRYPOINT ["python3", "server.py"]

EXPOSE 9999

