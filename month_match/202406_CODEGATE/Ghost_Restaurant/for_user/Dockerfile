FROM ubuntu:24.04@sha256:3f85b7caad41a95462cf5b787d8a04604c8262cdcdf9a472b8c52ef83375fe15

ENV prob_port 1337
ENV GLIBC_TUNABLES glibc.cpu.hwcaps=SHSTK

RUN apt-get update && apt-get install -y socat
ENV TERM=linux

RUN useradd -ms /bin/bash ctf

ADD ./flag.txt /flag
ADD ./share/chall /home/ctf

RUN chown -R root:ctf /home/ctf
RUN chmod -R 750 /home/ctf

WORKDIR /home/ctf
CMD socat -T 300 TCP-LISTEN:$prob_port,reuseaddr,fork EXEC:/home/ctf/chall,su=ctf
EXPOSE $prob_port
