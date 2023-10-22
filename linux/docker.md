# How to use Docker and migrate your existing Apps to your Linux Server?

References:

- [networkchuck](https://www.youtube.com/watch?v=iX0HbrfRyvc&t=12s)

- Christian Lempa: Video reference [youtube](https://www.youtube.com/watch?v=y0GGQ2F2tvs) and blog reference [github](https://github.com/christianlempa/videos/tree/main/docker-tutorial)

1. Docker Engine installation

After following instructions from [docs](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository). 

Run the following commands:

```bash
# Add user to the `docker` group to run docker commands:
sudo usermod -aG docker your_username

# Verify that the `docker.sock` file has appropriate permissions:
# It should be something like `srw-rw----`.
# The `docker.sock` file should be owned by the `docker` group.
ls -l /var/run/docker.sock

# If not, you can change the ownership:
sudo chown root:docker /var/run/docker.sock
```

2. Persistent Storage with Volumes

```bash
# If we run the container with a volume
docker run -p 80:80 -v nginx_data:/var/www/html -d nginx

# and remove the container
# the web server will still be available as we have attached a volume
# N/B: This is very useful for deployments
docker rm <container id>

# will display all volumes we have
# if we mount a new container to this volume, our data will still be there
docker volume ls
```

3. How to migrate data into Docker Container?

```bash
# To view data location
docker inspect nginx_data

# we are not allowed to access it from the host os
ls /var/lib/docker

# simulate an error then fix it
# Forbidden message
# create a `index.html` file under /var/www/html with a simple 'Hello World' header
# restart the container
docker run -p 80:80 -v /var/www/html:/var/www/html -d nginx
```

4. Manage Docker Resources with Portainer

