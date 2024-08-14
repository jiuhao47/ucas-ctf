FROM golang:1.18

RUN apt update
RUN apt install -y xinetd

RUN useradd ctf

COPY src /home/ctf
COPY flag /

WORKDIR /home/ctf

RUN go mod download && go mod verify

RUN go build -o main main.go

CMD ["/usr/sbin/xinetd","-dontfork"]