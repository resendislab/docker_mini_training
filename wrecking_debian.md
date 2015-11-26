## Wrecking a Debian system

Ok, since we are now familiar with docker let's party! We will now spectacularly 
destroy our Debian system. First we start a new Debian docker container with
`docker run`.

```bash
docker run -it --rm debian /bin/bash
```

Make sure you are inside your container (your prompt should contain some weird
numbers, the ID of the container). In my case it look like this:

```bash
root@4f3b533be9c3:/# 
```

Okay, let's go. HULK SMASH!

***Disclaimer: Do NOT try that at home (or better "at host").*** You should not 
have permissions to run the following commands in your host, but better safe than
sorry. Make sure you are inside the docker container (for instance run apt).

See all those nice basic programs in /bin?

```bash
ls /bin
```

Uuuuh that nice `date` program...

```bash
date
```

We will smash it!

```bash
echo "echo \"No time for you!\"" > /bin/date
```

Now try to run it...

```bash
date
```

Uuuuh, what are you gonna do? Run crying to your Mummy?
HULK SMASH MORE! Okay now let's try to delete everything!

```bash
rm -rf /
```

What do you think will happen? Nothing? Right, Debian will not let us delete the
entire OS, but it happily tells us how, so let's try the following one

```bash
rm -rf / --no-preserve-root
```

Okay that works but gives some errors that even as root we can not delete some
data in /sys. This is because sys does not only contain files but also hardware
access. Docker does never allow access to those parts of the host.

Well, now we are in a pickle. Most commands we know are gone, just try

```bash
cp
ls
mkdir
```

Hmm, that's weird. Some of the commands are still there!

```bash
echo "Ha! Puny Hulk cannot kill me!"
cd sys
cd ..
[ 3 > 2 ] && echo "TRUE!" 
```

Can you explain what happened?
