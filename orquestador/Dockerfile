FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends git curl ca-certificates \
    && install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc \
    && echo "deb [signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian bookworm stable" > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends docker-ce-cli \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
ARG REQS_HASH=1
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

CMD ["sleep", "infinity"]
