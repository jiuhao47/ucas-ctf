FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y openssh-server

RUN mkdir /run/sshd

COPY ./shared/sshd_config /etc/ssh/sshd_config
COPY ./shared/authorized_keys /etc/ssh/authorized_keys
COPY ./shared/motd /etc/motd

RUN chmod 600 /etc/ssh/authorized_keys


WORKDIR /chall

COPY ./shared/run.sh /chall/run.sh
COPY ./shared/validation /chall/validation

RUN chmod +x run.sh
RUN chmod +x validation

RUN useradd -u 1000 -d / -s /chall/run.sh user
RUN usermod -p '*' user
RUN chown -R user:user /chall
RUN chown user:user /etc/ssh/authorized_keys


CMD ["/usr/sbin/sshd", "-D", "-e", "-f", "/etc/ssh/sshd_config"]
