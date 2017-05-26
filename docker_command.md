## The docker command

Docker itself is mostly managed through one monolithic command called `docker`
(surprise!). There are some features of docker which can be misused. For that
reason docker usually requires root privileges to be run. If you use the MacOS
or Windows installation of docker you will not need to do anything. On those
platforms docker itself runs in a small (tiny, tiny, tiny) virtual machine which
has no connection to the host, so there is no way you could break it (so you can
be root there). If you installed Docker on linux you will either need to prefix
all the commands with `sudo` or your use must be added to the `docker` group.
This can be achieved in Ubuntu/Debian with (requires restart of the docker service)

```bash
sudo useradd -aG docker username
```
However, careful with that! You should consider any user in the docker group
a super-user. From now on we will assume you have the rights to use docker. If
any of the following commands give you a permission of missing socket error
just prefix `sudo`.

## Getting started

First let's check if the installation went fine. On MacOS and Windows look
for the Docker Quick Start Terminal and fire it up. On Linux, open a Terminal
and type `docker` (or `sudo docker`). This will give you the following output:

```
Usage: docker [OPTIONS] COMMAND [arg...]
       docker daemon [ --help | ... ]
       docker [ --help | -v | --version ]

A self-sufficient runtime for containers.

Options:
...

Commands:
    attach    Attach to a running container
    build     Build an image from a Dockerfile
...
    volume    Manage Docker volumes
    wait      Block until a container stops, then print its exit code

Run 'docker COMMAND --help' for more information on a command.
```

So you can see that there is quite a lot that can be done with the `docker`
command usually by using `docker subcommand`.

There are two important concepts we have to grasp in Docker, images and containers.
We have already met containers in introduction. They are small isolated parts on
your file system that contain a small operating system together with its own
file system (called "volume" in docker). An image can be seen as a rule how
a container should look like. It is an immutable snapshot of the default configuration
of the container. As such an image is something you build once. From each image you
can generate an infinite number of containers in which you run stuff or do whatever
you want. So TL;DR: we create containers from images. Docker provides an online
repository at https://hub.docker.com of many images (>600.000 atm). You can download
any of the images with `docker pull`. So we will now download a minimal image
of the latest Debian 8 (Jessie).

```bash
docker pull debian
```

After downloading let's check whether we got the image with

```bash
docker images
```

Jup, that is our Debian image. See how small it is? This is because docker uses
the kernel of the host system. So there is no need for the kernel, drivers or
any boot infrastructure. To create a container from an image and run it we use
`docker run`. The `run` command requires at least two things: the name of an image
and the command to run within the container. So let us run the bash shell in our
brand new debian image (you might have to press Enter again after running).

```bash
docker run debian /bin/bash
```

Okay, that just returns us to our shell. What happened. Well, maybe the container
is running in the background? We can use `docker ps` to see all running containers.

```bash
docker ps
```

Nope, nothing here. Okay, let's try the `-a` flag which allows us to see all
living or dead containers.

```bash
docker ps -a
```

Hey here is our container! And it even got a nice random name! But why does it
say exited? Well, we started bash in a non-interactive mode. So bash will run
all given commands (none in our case) and exit. Pffffff, what a disappointment.
Now we have that large useless container on our disk. Let's get rid of it. Do
you remember the cute name? Use it!

```bash
docker rm -v cute_name
docker ps -a
```

Okay, it's gone. Did you notice the `-v` option? By default `docker rm` will
remove the container but not the file system (the *v*olume). With `-v` we tell
docker to delete the volume as well and prevents pollution of our file system.

Well, let's try again with our Debian. This time we will add two option flags
`-it` to run the container in interactive pseudo-TTY mode, and `--rm` to automatically
delete the container and its volumes upon exiting.

```bash
docker run -it --rm debian /bin/bash
```

That drops you into the bash shell of the Debian container. Yeiih. Well let us
first check whether we are really working with Debian here. In that shell let us
install some stuff.

```bash
apt update
apt install screenfetch cowsay
```

Okay, that looks like the Debian package manager. Let us verify for sure with
screenfetch.

```bash
screenfetch
```

Or do you rather trust cows?

```bash
/usr/games/cowsay "Yep it's Debian! MOOOOOOOO!"
```

Did you notice that you did not need to type `sudo` to install packages? In
a docker container you are usually root. Finally, to get out of the shell you can
use Ctrl+D. And you're back in your host system.

Let's see what we have learned.

- controlling Docker with the `docker` command
- getting images from Docker Hub
- running and deleting containers
- getting a list of available images, running/stopped containers
