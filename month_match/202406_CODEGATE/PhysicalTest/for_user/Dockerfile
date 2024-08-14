FROM ubuntu:22.04@sha256:a6d2b38300ce017add71440577d5b0a90460d0e57fd7aec21dd0d1b0761bbfb2

RUN apt-get update -y
RUN apt-get install -y qemu-system python3-pip cpio
RUN apt-get install -y xinetd
RUN apt-get install -y netcat
RUN apt-get install -y wget
RUN apt-get install -y gzip
RUN python3 -m pip install requests

RUN useradd --create-home --shell /bin/bash ctf

WORKDIR /home/ctf

ADD ./share /home/ctf

RUN chmod +x pow.py
RUN chmod +x run.sh
RUN chmod +x ynetd

CMD ./ynetd -p 4132 "timeout 60 python3 pow.py"

