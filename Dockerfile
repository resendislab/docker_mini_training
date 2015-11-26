FROM debian
MAINTAINER "Weird friend"

RUN apt-get -y update && apt-get -y install cowsay
RUN cd /bin && ln -s /usr/games/cowsay 

ENTRYPOINT ["/bin/cowsay", "-f", "vader"]
