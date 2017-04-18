FROM gitlab/gitlab-runner:latest

MAINTAINER mm@pfcta.com

# ---------- Python Install ----------#
RUN apt-get update && apt-get install -y \
    build-essential \
    python \
    python-dev \
    libpython2.7-dev \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# ---------- Gitlab Runner Setup ---------- #
ENV GITLAB_URL https://gitlab.com
ENV GITLAB_REGISTRATION_TOKEN xxx-xxx-xxx
ENV DOCKER_IMAGE python:3.5
ENV DOCKER_IMAGE_DESCRIPTION python-3.5

ADD gitlab-runner.py /gitlab-runner.py
RUN chmod +x /gitlab-runner.py

ENTRYPOINT ["./gitlab-runner.py"]
