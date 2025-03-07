# Use the specified base image
FROM codercom/code-server:4.16.1

# Switch to root user for permissions
USER root

# Install Node.js v18 along with python3-dev and python3-pip
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get update && \
    apt-get install -y nodejs python3-dev python3-pip

# Copy the requirements file to the container
COPY requirements.txt /tmp/

# Install Python packages from the requirements file
RUN python3 -m pip install -r /tmp/requirements.txt

# Switch to coder user
USER coder

# Set npm global prefix and update PATH for the coder user
RUN npm config set prefix /home/coder/.npm-global
ENV PATH=/home/coder/.npm-global/bin:$PATH

# Install the Visual Studio Code extensions
RUN code-server --install-extension ms-toolsai.jupyter@2023.4.1001091014 \
                --install-extension ms-toolsai.vscode-jupyter-powertoys \
                --install-extension ms-python.python

# Install wscat globally using npm
RUN npm install -g wscat --unsafe-perm=true

# Start code-server in password authentication mode
CMD ["code-server", "--auth=password"]