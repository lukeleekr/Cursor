# Use the official Microsoft devcontainer base image with Node.js 20
FROM mcr.microsoft.com/devcontainers/javascript-node:20

# Install Python 3.11+ and common tools
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    python3.11 \
    python3-pip \
    git \
    curl \
    wget \
    vim \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Set Python 3.11 as default python3
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Install global npm packages if needed (optional)
# RUN npm install -g yarn pnpm

# Set the default shell to bash
SHELL ["/bin/bash", "-c"]


