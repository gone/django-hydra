FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


FROM node:20-slim as js-builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# In your main stage:

FROM python:3.13-slim-bookworm
# Copy the application from the builder
COPY --from=builder --chown=app:app /app /app
COPY --from=js-builder /app/sampleapp/static_source/assets /app/sampleapp/static_source/assets
COPY --from=js-builder /app/sampleapp/static_source/manifest.json /app/sampleapp/static_source/

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"
RUN python /app/manage.py collectstatic --noinput --settings sampleapp.config.settings.build
EXPOSE 8000

CMD ["gunicorn"]
