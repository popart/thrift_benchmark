FROM ubuntu:12.04

RUN apt-get update
RUN apt-get install -y ant make
RUN apt-get install -y libboost-dev libboost-test-dev libboost-program-options-dev libboost-filesystem-dev libboost-thread-dev libevent-dev automake libtool flex bison pkg-config g++ libssl-dev

RUN apt-get install -y python
RUN apt-get install -y python-pip python-dev build-essential 
RUN pip install --upgrade pip
RUN pip install --upgrade virtualenv

RUN apt-get install -y golang-go
RUN apt-get install -y wget

WORKDIR /home
RUN wget http://apache.cs.utah.edu/thrift/0.10.0/thrift-0.10.0.tar.gz
RUN tar -xvf thrift-0.10.0.tar.gz 

WORKDIR /home/thrift-0.10.0
RUN ./configure
RUN make
RUN make install

RUN pip install thrift

WORKDIR /home

RUN apt-get install -y vim
