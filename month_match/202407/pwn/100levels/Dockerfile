FROM pwn.red/jail
COPY --from=ubuntu:18.04 / /srv
RUN mkdir /srv/app
COPY libc.so /srv/lib
COPY 100levels /srv/app/run
COPY flag.txt /srv/flag
ENV JAIL_TIME=120 JAIL_POW=0
