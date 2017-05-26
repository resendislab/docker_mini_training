# Data persistence with Docker volumes

Docker manges persistent data in volumes. Basically, there are two kinds of
volumes:

1. managed volumes that are the used by your containers and that have some
   layer management to reduce disk usage
2. unmanaged volumes that can be shared between containers or containers and
   the host and should be used for storing large objects

One of the common pitfalls when using docker is assuming that your data in
containers is safe. Data in conatiners itself should be assumed short lived
such as log files etc. Let's illustrate this.

```bash
docker run -it debian
mkdir /data && cd data
echo "It's alive!" > frankenstein.txt
cat frankenstein.txt
exit
```

Where is the file now? Well actually it's not lost. As long as we don't delete
the container the managed file system is still there and we could recover it.

```bash
docker start prickly_perlman  # That's the name I got
docker attach prickly_perlman
cat /data/frankenstein.txt
exit
docker rm prickly_perlman
```

However in the moment we remove the container the data is gone. A much nicer
way is to create a custom volume for the data. A volume is a data container and
usually simply a pretty thin wrapper arounf your local file system. However, it
may use a myriad of different volume drivers, for instance it could also be
a file on Hadoop, data in the cloud and many more. Volumes in docker can be
managed with the `volume` subcommand.

```bash
docker volume ls
```

Currently, there is nothing. So let's create something. Since volumes are just
data without any API you will need a container to write to it. Volume mapping
in docker is realized with the `-v` option and has the syntax
`name_or_path:path_in_container` (the `outside:inside` is pretty common in
docker). For now we will only give a name which will create a new volume on
our local disk.

```bash
docker run -it --rm -v my_data:/data debian
cd data
echo "It's alive!" > frankenstein.txt
exit
docker rm name

docker volume ls
```

As we see we have created a new data volume and our data is kept safe in there.
We can attack the data volume to any one or even several containers afterwards.

```bash
docker run -it --rm -v my_data:/data debian
cat /data/frankenstein.txt
```

Sharing volumes is a pretty cool feature. For instance you can have many
containers write log files or backups to the same location. You can remove
volumes with `docker volume rm`

```bash
docker volume rm my_data  # all clean now :D
```

Instead of using data volumes you can also directly map locations between
the host and the container. Just let the "inside" part be a complete
**existing** path.

```bash
mkdir test
docker run -it --rm -v /home/my_user/test:/test debian
echo "I'm flying through walls booooooo" > /test/ghost.txt
exit
```

Okay, the file is also mirrored on the host. So now use `ls` to see who the
file belongs to... Wow, it's from `root`. This is why volume mapping is probably
one of dockers most dangerous feature. In a mapped volume you may be root and
can edit or delete at your leisure. This is why you should consider everybody
in the "docker" group to be an admin.
