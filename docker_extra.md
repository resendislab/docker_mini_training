## And some more docker...

Okay, we now have some basic grasp of how to run docker. However, we still do not
know how images are **actually** created. So let us build one. We have seen before
that we can run our Debian container and install some software to it. We also
now that without the `--rm` flag the container will persist. That is a good
start let us use this.

By now we are huge fans of the `cowsay` program and want the entire world to be
be able to express themselves through a cow. That is why we want an official
cowsay docker image out there. So let us start by running our Debian image
again and installing cowsay. We will also link cowsay directly into /bin because
in our Docker container cows are first class citizens.

```bash
docker run -it debian /bin/bash

# Now inside the container
apt update && apt install cowsay
cd /bin && ln -s /usr/games/cowsay
# Quit with Ctrl-D
```

By the way you can get back into the shell of the container with 
`docker start -ia cute_name`. 

So now we have a container with cowsay installed. But how do we create an image
from that? Easy peasy, with `docker commit`.

```bash
docker commit -a "My Name" cute_name cowsay
```

The `-a` flag allows you to define a mantainer for the image and the last argument
to the command is the name of the image. If you had a (free) Docker Hub account you 
could now send the image to docker hub with `docker push`. Well done!

Now, you have that friend who is a huge fan of Star Wars and cows and wants to
change your image to have a Darth Vader cow saying things. You do not want to change
your image but your friend has no idea how to install stuff in Debian. Wouldn't
it be peachy if you could create some small file with build instructions that
your friend could modify to build his own cowsay image? Well that is what
Dockerfiles are for! We will not go into too much details, because you can easily
read all there is to know about Dockerfiles at http://docs.docker.com/engine/reference/builder/.

So you send your friend the following Dockerfile:

```Dockerfile
FROM debian
MAINTAINER "Your Name"

RUN apt-get -y update && apt-get -y install cowsay
RUN cd /bin && ln -s /usr/games/cowsay 

ENTRYPOINT ["/bin/cowsay"]
```

`FROM` defines the base image you want to use and `RUN` runs any command you want 
inside of the docker container. There will be now interactive shell so all commands
have to run without confirmations. This is why we use `apt-get -y` which replies
"yes" to all necessary confirmations. The `ENTRYPOINT` defines a default command for the
container so that having your cow say "Hello!" is as easy as `docker run --rm cowsay "Hello!"`.

Your friend can now easily build his own image by changin into the directory
with the Dockerfile and typing 

```bash
docker build -t vadercow .
```

This will pull all the necessary images and build his vadercow image. Your friend
is happy to see that the following works

```
docker run vadercow "I am still a cow"
```

He makes the following adjustment to the build file

```Dockerfile
FROM debian
MAINTAINER "Weird friend"

RUN apt-get -y update && apt-get -y install cowsay
RUN cd /bin && ln -s /usr/games/cowsay 

ENTRYPOINT ["/bin/cowsay", "-f", "vader"]
```
and is delighted to see his Vader cow when running

```bash
docker run --rm vadercow "Hello Weird Friend!"
``` 

Dockerfiles are not only practical to define standardize images but they can also
be used for automated builds. You can connect Dockerfile from a Github repository 
to your Docker Hub account so that upon any changes in your Dockerfile the
Docker Hub will build your image on their servers and provide it for downloads.
For an example see https://hub.docker.com/r/cdiener/spocker/builds.
