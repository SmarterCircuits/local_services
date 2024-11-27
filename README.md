# local_services
Configuration, install files, and commands for Smarter Circuits local services episode.

# COMMANDS:
## Portainer installation:
docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:2.21.4

# Notes on installing Technitium:
Use the tchnitium-docker-compose.yml (called just docker-compose.yml in its own directory) and docker compose up -d

## If you run into the port is use issue:
sudo systemctl stop systemd-resolved
sudo systemctl disable systemd-resolved

