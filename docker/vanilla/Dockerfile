ARG PY_TAG
FROM python:${PY_TAG} as vanilla
LABEL maintainer="CADIC Jean"

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Asia/Tokyo \
    PYTHONPATH=/workspace

RUN apt-get update && apt-get install -y \
    git \
    curl \
    nano \
    npm \
    pylint \
    sudo

# Install vite
RUN npm install -g vite

# Install task
RUN sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin

# uv
ADD --chmod=755 https://astral.sh/uv/install.sh /tmp/install.sh
RUN /tmp/install.sh && rm /tmp/install.sh && mv /root/.local/bin/uv /usr/local/bin/uv

WORKDIR /workspace

FROM vanilla as dev

RUN apt-get update && apt-get install -y \
    glances \
    pre-commit

# foo
RUN adduser --disabled-password --gecos '' foo
RUN adduser foo sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN chown -R foo:foo /home/foo
