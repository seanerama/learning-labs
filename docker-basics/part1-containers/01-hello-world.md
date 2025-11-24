# Lesson 1: Hello World

Your first Docker container!

## 🎯 Objective

Run the official Docker "hello-world" container to verify your installation and understand the basics of how Docker works.

## 📝 What You'll Learn

- How to run your first container
- What happens when you run `docker run`
- How Docker pulls images from Docker Hub
- Understanding container output

## 🚀 Steps

### Step 1: Run Hello World

```bash
docker run hello-world
```

### Step 2: Understand What Happened

When you ran that command, Docker did the following:

1. **Checked locally** for the `hello-world` image
2. **Didn't find it**, so contacted Docker Hub
3. **Downloaded** (pulled) the image
4. **Created** a container from the image
5. **Ran** the container
6. **Displayed** the output
7. **Exited** the container

### Step 3: Examine the Output

You should see something like:

```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
2db29710123e: Pull complete
Digest: sha256:...
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

...
```

### Step 4: Run It Again

```bash
docker run hello-world
```

**Notice:** This time it's faster! Why?

The image is already downloaded, so Docker:
1. Skips the pull step
2. Creates a new container from the local image
3. Runs it
4. Exits

### Step 5: Check Downloaded Images

```bash
docker images
```

Output:
```
REPOSITORY    TAG       IMAGE ID       CREATED         SIZE
hello-world   latest    feb5d9fea6a5   15 months ago   13.3kB
```

You now have the `hello-world` image stored locally!

### Step 6: Check Containers

```bash
# List running containers (should be empty)
docker ps

# List ALL containers (including stopped ones)
docker ps -a
```

Output:
```
CONTAINER ID   IMAGE         COMMAND    CREATED          STATUS                      PORTS     NAMES
abc123def456   hello-world   "/hello"   2 minutes ago    Exited (0) 2 minutes ago              determined_darwin
def456abc789   hello-world   "/hello"   5 minutes ago    Exited (0) 5 minutes ago              peaceful_tesla
```

**Notice:**
- You ran the container twice, so there are 2 stopped containers
- Each got a random name (determined_darwin, peaceful_tesla)
- Status shows "Exited (0)" meaning it finished successfully

## 🧪 Experiments

### Experiment 1: Name Your Container

Instead of random names, give it a specific name:

```bash
docker run --name my-first-container hello-world
```

Check it:
```bash
docker ps -a
```

### Experiment 2: Automatic Cleanup

Use `--rm` to automatically remove the container after it exits:

```bash
docker run --rm hello-world
```

Check containers:
```bash
docker ps -a
```

It's not there! The `--rm` flag deleted it automatically.

### Experiment 3: Clean Up

Remove the stopped containers:

```bash
# Remove by name
docker rm my-first-container

# Remove all stopped containers at once
docker container prune
```

## 💡 Key Concepts

### Images vs Containers

| Image | Container |
|-------|-----------|
| Blueprint/Template | Running instance |
| Stored on disk | Running in memory |
| Static, doesn't change | Can be modified while running |
| Created once | Can create many from one image |

Think of it like:
- **Image** = Recipe
- **Container** = Meal made from recipe

### Docker Run Workflow

```
docker run hello-world
        │
        ▼
Is image local? ──No──> Pull from Docker Hub
        │                       │
       Yes                      │
        │                       │
        └───────────┬───────────┘
                    ▼
            Create container
                    │
                    ▼
            Run container
                    │
                    ▼
            Show output
                    │
                    ▼
            Container exits
```

### Container Lifecycle

```
Created → Running → Stopped → Removed
   ▲         │
   └─────────┘ (restart)
```

## 📊 Command Breakdown

```bash
docker run hello-world
│      │   │
│      │   └─── Image name
│      └─────── Sub-command (run a container)
└──────────────── Docker command
```

With options:
```bash
docker run --name my-container --rm hello-world
│      │   │                    │   │
│      │   │                    │   └─── Image
│      │   │                    └─────── Auto-remove when exits
│      │   └──────────────────────────── Give it a name
│      └──────────────────────────────── Run command
└──────────────────────────────────────── Docker
```

## ✅ Verification

You should now be able to:
- [x] Run the hello-world container
- [x] Understand what happens during `docker run`
- [x] List images with `docker images`
- [x] List containers with `docker ps -a`
- [x] Name containers with `--name`
- [x] Auto-remove containers with `--rm`
- [x] Clean up stopped containers

## 🎯 Practice

Try these commands:

```bash
# 1. Pull an image without running it
docker pull alpine

# 2. List your images
docker images

# 3. Run alpine (it just exits immediately)
docker run alpine

# 4. Run alpine with a command
docker run alpine echo "Hello from Alpine!"

# 5. Run alpine interactively
docker run -it alpine sh

# Inside alpine, try:
ls
pwd
cat /etc/os-release
exit

# 6. Clean up
docker ps -a
docker container prune
```

## ❓ FAQ

**Q: Why did the container exit immediately?**
A: The hello-world container is designed to print a message and exit. Containers run only as long as their main process runs.

**Q: Where is the image stored?**
A: On your local machine in Docker's storage location:
- Linux: `/var/lib/docker/`
- Mac: Inside Docker Desktop's VM
- Windows: Inside WSL2 or Docker Desktop

**Q: Can I run multiple containers from one image?**
A: Yes! You can create unlimited containers from a single image.

**Q: Do stopped containers take up space?**
A: Yes! They take up disk space. Use `docker container prune` to clean up.

## 🔗 Related Commands

```bash
docker images              # List downloaded images
docker ps                  # List running containers
docker ps -a              # List all containers
docker run <image>        # Run a container
docker run --rm <image>   # Run and auto-remove
docker run --name <name> <image>  # Run with specific name
docker container prune    # Remove all stopped containers
docker rm <container>     # Remove specific container
```

## 📚 What's Next?

Now that you understand the basics, let's run something more interesting!

**Next Lesson:** [02 - Web Server →](02-web-server.md)

In the next lesson, you'll run a web server and access it from your browser!

---

**Lesson Duration:** 10 minutes
**Difficulty:** Beginner
**Prerequisites:** Docker installed
