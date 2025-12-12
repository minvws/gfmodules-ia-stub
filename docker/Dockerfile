# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}-bookworm AS base

ARG PROJECT_DIR="/src" \
    LOCAL_SOURCE_DIR="." \
    NODE_VERSION=22 \
    APP_USER="app" \
    APP_GROUP="app" \
    NEW_UID=1000 \
    NEW_GID=1000 \
    INSTALL_NPM_ASSETS=true
    
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_CACHE_DIR=/tmp/poetry-cache \
    POETRY_VIRTUALENVS_CREATE=false

# Create a non-privileged user that the app will run under.
RUN groupadd --system ${APP_GROUP} --gid=${NEW_GID} && \
  adduser \
  --disabled-password \ 
  --gecos "" \
  --uid ${NEW_UID} \
  --gid ${NEW_GID} \
  ${APP_USER}

RUN apt update && \
    apt install -y \
    curl \
    iputils-ping \
    git \
    gnupg2 \
    libxmlsec1-dev \
    pkg-config \
    lsb-release \
    make \
    && curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION}.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

RUN pip3 install --upgrade pip && \
    pip3 install poetry --no-cache-dir

FROM base AS builder

WORKDIR ${PROJECT_DIR}

# setup npm
RUN mkdir -p node_modules static/assets
COPY dist/scripts/setup-npm.sh vite.config.js package.json package-lock.json ./
COPY /dist/resources ./dist/resources
RUN --mount=type=secret,id=npmrc,target=${PROJECT_DIR}/.npmrc \
    if [ "$INSTALL_NPM_ASSETS" = "true" ]; then \
        chmod +x setup-npm.sh && ./setup-npm.sh; \
        npm run build; \
    fi

# setup python environment
COPY ./pyproject.toml ./poetry.lock ./poetry.toml ./
RUN --mount=type=cache,target=${POETRY_CACHE_DIR} \
    --mount=type=ssh \
    mkdir -p -m 0700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts && \
    poetry install --no-interaction --no-root

FROM base AS final

ARG PYTHON_VERSION

COPY --chown=${APP_USER}:${APP_GROUP} --from=builder /usr/local /usr/local
RUN chown -R ${APP_USER}:${APP_GROUP} /usr/local/lib/python${PYTHON_VERSION}/site-packages

ENV PATH="/usr/local/bin:$PATH"

WORKDIR ${PROJECT_DIR}
EXPOSE 8006

COPY --chown=${APP_USER}:${APP_GROUP} ${LOCAL_SOURCE_DIR}/ ${PROJECT_DIR}
COPY --from=builder --chown=${APP_USER}:${APP_GROUP} ${PROJECT_DIR}/node_modules ${PROJECT_DIR}/node_modules
COPY --from=builder --chown=${APP_USER}:${APP_GROUP} ${PROJECT_DIR}/static/assets ${PROJECT_DIR}/static/assets

USER ${APP_USER}

CMD ["tail", "-f", "/dev/null"]
