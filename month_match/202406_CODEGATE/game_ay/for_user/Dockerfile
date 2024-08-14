FROM python:3.11

RUN apt-get update -y
RUN apt-get install -y xinetd

COPY ./xinetd /etc/xinetd.d/gamesay

RUN useradd -m -u 1000 gamesay

COPY ./src /src

RUN chown -R gamesay:gamesay /src
RUN chmod 775 /src/run.sh

WORKDIR /src

CMD ["/usr/sbin/xinetd","-dontfork"]

