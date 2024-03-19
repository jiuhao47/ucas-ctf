FROM lewinc/activemq:5.18.2
COPY flag /flag
COPY readflag /readflag
USER root
RUN set -ex && apt-get update \
  && apt-get install -y lib32z1 zip acl \
  && apt-get install -y build-essential manpages-dev\
  && chmod u=srx,g=rx,o=rx /readflag \
  && chmod 400 /flag
USER activemq
EXPOSE 61616


