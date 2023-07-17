#!/bin/bash

# Function to generate SSH key pair
generate_ssh_key() {
  local ssh_dir=$1
  ssh-keygen -t rsa -b 4096 -N "" -f "$ssh_dir/id_rsa"
}

# Function to generate GPG key pair
generate_gpg_key() {
  local gpg_dir=$1
  local name="Generated Key"
  local email="generated@example.com"

  # Set GPG user details
  echo "%echo Generating a GPG key" > "$gpg_dir/gpg_gen_batch"
  echo "Key-Type: RSA" >> "$gpg_dir/gpg_gen_batch"
  echo "Key-Length: 4096" >> "$gpg_dir/gpg_gen_batch"
  echo "Key-Usage: sign" >> "$gpg_dir/gpg_gen_batch"
  echo "Name-Real: $name" >> "$gpg_dir/gpg_gen_batch"
  echo "Name-Email: $email" >> "$gpg_dir/gpg_gen_batch"
  echo "Expire-Date: 0" >> "$gpg_dir/gpg_gen_batch"
  echo "Passphrase: ''" >> "$gpg_dir/gpg_gen_batch"
  echo "%commit" >> "$gpg_dir/gpg_gen_batch"
  gpg --batch --generate-key "$gpg_dir/gpg_gen_batch"
  rm "$gpg_dir/gpg_gen_batch"
}

# Check if the number of arguments is correct
if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <directory> [OPTIONS]"
  echo "Options:"
  echo "  --ssh (-s)  Generate SSH key pair"
  echo "  --gpg (-g)  Generate GPG key pair"
  exit 1
fi

# Parse command-line arguments
directory=""
generate_ssh=false
generate_gpg=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    -s | --ssh )
      generate_ssh=true
      shift
      ;;
    -g | --gpg )
      generate_gpg=true
      shift
      ;;
    * )
      directory="$1"
      shift
      ;;
  esac
done

# Check if the specified directory exists
if [[ ! -d "$directory" ]]; then
  echo "Error: The specified directory does not exist."
  exit 1
fi

# Generate SSH key if the option is set
if [[ "$generate_ssh" == true ]]; then
  ssh_dir="$directory/ssh_keys"
  mkdir -p "$ssh_dir"
  generate_ssh_key "$ssh_dir"
  echo "SSH Public Key:"
  cat "$ssh_dir/id_rsa.pub"
fi

# Generate GPG key if the option is set
if [[ "$generate_gpg" == true ]]; then
  gpg_dir="$directory/gpg_keys"
  mkdir -p "$gpg_dir"
  generate_gpg_key "$gpg_dir"
  echo "GPG Public Key:"
  gpg --armor --export "$name <$email>"
fi
