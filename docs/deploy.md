Deploy
========


Development
--------


Production
--------

```
# Create the droplet
docker-machine create --driver digitalocean --digitalocean-access-token=X screenshot-server

# Use the machine
eval $(docker-machine env screenshot-server)

# Create the network
docker network create nginx-proxy

# Deploy
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```


