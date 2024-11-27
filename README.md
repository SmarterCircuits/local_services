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

# AdGuard install command (the one I used in the video):
docker run --name adguardhome\
    --restart unless-stopped\
    -v /srv/adguard/workdir:/opt/adguardhome/work\
    -v /srv/adguard/confdir:/opt/adguardhome/conf\
    -p 553:53/tcp -p 53:53/udp\
    -p 67:67/udp -p 68:68/udp\
    -p 80:80/tcp -p 443:443/tcp -p 443:443/udp -p 3000:3000/tcp\
    -p 853:853/tcp\
    -p 784:784/udp -p 853:853/udp -p 8853:8853/udp\
    -p 5443:5443/tcp -p 5443:5443/udp\
    -d adguard/adguardhome

# KIWIX Install Command (see their site for zim files at https://library.kiwix.org/):
docker run -v /home/ian/kiwix:/data -p 8080:8080 ghcr.io/kiwix/kiwix-serve '*.zim'

# Notes on installing the FLask API container:
You need both the docker-componse.yml and the requirements.txt file

