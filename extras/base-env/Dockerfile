FROM ubuntu:23.10
RUN cat /etc/resolv.conf

## Install base ubuntu packages
RUN apt-get update && apt-get install -y \
    sudo \
    curl \
    gpg \
    git \
    tig \
    jq \
    fish

## Install Tailscale
RUN curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/focal.gpg | gpg --dearmor -o /usr/share/keyrings/tailscale-archive-keyring.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/tailscale-archive-keyring.gpg] https://pkgs.tailscale.com/stable/ubuntu focal main" | tee /etc/apt/sources.list.d/tailscale.list
RUN apt-get update && apt-get install -y tailscale

## Pos build clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

## Prepare container entrypoint
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
