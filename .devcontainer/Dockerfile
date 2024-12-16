FROM mcr.microsoft.com/devcontainers/python:1.1-3.11

# RUN sudo apt update && \
    # geckodriver
    # wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz && \
    # tar -xvzf geckodriver* && \
    # chmod +x geckodriver && \
    # mv geckodriver /usr/local/bin/ && \
    # other packages
    # sudo apt install -y \
    # firefox-esr \
    # speech-dispatcher \
    # tmux && \
    # install poetry
    # pip install poetry==1.1.13 
    # echo "hello world"

RUN sudo apt update && \
    pipx install poetry==1.8.3

# # Copy .gitconfig
# COPY ~/.gitconfig /home/vscode/.gitconfig

# # Set correct ownership and permissions
# RUN chown vscode:vscode /home/vscode/.gitconfig && \
#     chmod 644 /home/vscode/.gitconfig

# # Set the safe.directory in git config
# RUN git config --global --add safe.directory /workspaces/research-crew

# # Switch back to the vscode user
# USER vscode