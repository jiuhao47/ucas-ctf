FROM ubuntu:16.04

#RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list && \
RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y lib32z1 xinetd iputils-ping

RUN useradd -u 1000 -m ctf

WORKDIR /home/ctf

RUN cp -R /lib* /home/ctf && \
    cp -R /usr/lib* /home/ctf

RUN mkdir /home/ctf/dev && \
    mknod /home/ctf/dev/null c 1 3 && \
    mknod /home/ctf/dev/zero c 1 5 && \
    mknod /home/ctf/dev/random c 1 8 && \
    mknod /home/ctf/dev/urandom c 1 9 && \
    chmod 666 /home/ctf/dev/*
    
RUN mkdir /home/ctf/etc && \
    cp /etc/passwd /home/ctf/etc


RUN mkdir /home/ctf/bin && \
    cp /bin/sh /home/ctf/bin && \
    cp /bin/ls /home/ctf/bin && \
    cp /bin/cat /home/ctf/bin && \
    cp /bin/ping /home/ctf/bin && \
    cp /bin/uname /home/ctf/bin && \
    cp /bin/df /home/ctf/bin && \
    cp /bin/date /home/ctf/bin && \
    cp /usr/bin/whoami /home/ctf/bin && \
    cp /usr/bin/id /home/ctf/bin && \
    cp /bin/pwd /home/ctf/bin && \
    cp /sbin/poweroff /home/ctf/bin

COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./start.sh /start.sh
RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail

RUN chmod +x /start.sh

COPY ./bin/ /home/ctf/
RUN chown -R root:ctf /home/ctf && \
    chmod -R 750 /home/ctf && \
    chmod 740 /home/ctf/flag

CMD ["/start.sh"]

EXPOSE 9999
