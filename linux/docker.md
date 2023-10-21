# Docker Engine installation

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
