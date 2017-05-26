# Networking in docker

Networking in docker is pretty powerful even though most people never want to
get beyond "-p 8000:8000" :D In fact, docker manges it's own network stack and
a fresh docker installation comes with three configured networks out of the
box...

Networks in docker can be managed with the `network` subcommand. For instance
we can list all current networks:

```bash
docker network ls
```

Here we see the three default networks:

- "bridge": An isolated network in which containers can only see each other.
- "host": The network of our host.
- "none": A mock network in which each container is completely isolated and only
          sees itself.

So we will now use a docker image that actually runs a web app so we can see
what happens in the network. We will run a jupyter notebook server (without
a password for now).

```bash
docker pull jupyter/minimal-notebook
docker run -d jupyter/minimal-notebook start-notebook.sh --NotebookApp.token=''
docker ps
```

So we see the container exposes the port 8888. But how do we get access to
that? By default the container runs in the bridge network. We can "publish"
the app to our host with the `-p` option of docker run. The syntax is `host_port:container_port` (see, again "outside:inside"). Let's kill the app and
try again:

```bash
docker rm -f gigantic_brown

docker run -d -p 8888:8888 jupyter/minimal-notebook start-notebook.sh --NotebookApp.token=''
docker ps
```

Open you browser at 0.0.0.0:8888 and *tada* the app is running (if you use the
docker toolbox you need to use the IP of your docker vm instead). So this is
already pretty powerfull since we could run several instances of the app and
publish it two different IPs on the host. But we don't have to do this at all.

The bridge network in docker has it's own IP range. We can see that with the
`inspect` command.

```bash
docker network inspect bridge
```

This gives us the current network configuration. Can you see the entry for our
jupyter container? It actually has its own IP in the bridge network
(172.17.0.2 in my case). So now open your browser at 172.17.0.2:8888 and *tada*
our app is there again. When using the bridge network IP you would not even
need to use the "publish" option `-p`. So yeah, you get an entire emulated network
stack in which you can interconnect apps as you wish, but whatever :D You can
stop and remove the jupyter server now.

It can actually get better. We can also create new networks to connect a specific
subset of containers. This is done with the `create` sub-subcommand.

```bash
docker network create my_net
docker network ls
```

So we see we have created a new network. We can launch containers into our new
network using the `--network` option of docker run. We will launch two
containers: a jupyter app server and a simple debian one.

```bash
docker run -d --name= jupyter --network=my_net jupyter/minimal-notebook start-notebook.sh --NotebookApp.token=''
docker run -it --rm --name=debian --network debian
```

Note how we gave names to both containers. The cool thing about custom bridge
networks is that they automatically configure the DNS to use the container
names. So in the Debian conatiner we can now simply do

```bash
ping -w 4 jupyter
ping -w 4 debian
```

This is pretty neat and can be used to setup complex network stacks on a single
machine. Containers may contain to several networks at once so you can set up
complex layered network architectures as well. Docker also has olverlay
networks which can connect several physical hosts into a single network. However,
if you want that functionality you should probably look into Kubernetes or
Docker Swarm.
