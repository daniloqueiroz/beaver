#!/bin/bash

function log() {
  level=$1
  shift
  echo -e "::$level=> $*"
}

function start_tailscale() {
  log info Starting Tailscale
  # Start tailscaled in the background
  tailscaled --tun=userspace-networking --socks5-server=localhost:1055 --outbound-http-proxy-listen=localhost:1055 &
  # Wait for tailscaled to initialize
  sleep 5s
  # Run tailscale up with the auth key
  tailscale up --authkey="$1" --ssh --accept-routes
}

function sync_files() {
  cp -rf "$1" .
}

log info Initializing dev container
[ -n "$BASE_FILES_SRC" ] && sync_files "$BASE_FILES_SRC"
[ -n "$TS_AUTH_KEY" ] && start_tailscale "$TS_AUTH_KEY"
[ -n "$GIT_REPO" ] && git clone "$GIT_REPO"

asdf install

while true; do
  # TODO poll the controler api to know when to stop
  sleep 60s
done

[ -n "$TS_AUTH_KEY" ] && tailscale logout