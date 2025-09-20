
# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS uv


# Clone the repository and checkout the branch
WORKDIR /app


# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev --no-editable


# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable


RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable

FROM python:3.13-slim-bookworm



# Create a non-root user
RUN groupadd --gid 1000 mcp_user && \
    useradd --uid 1000 --gid mcp_user --shell /bin/bash --create-home mcp_user

WORKDIR /app

# Copy the virtual environment from uv build stage
#COPY --from=uv /root/.local /home/mcp_user/.local
COPY --from=uv /app/.venv /app/.venv

# Change ownership of the virtual environment and app to mcp_user
RUN chown -R mcp_user:mcp_user /app/.venv /app 

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Switch to non-root user
USER mcp_user


#CMD ["python", "-m", "azuredevops_tools.main"]
CMD ["azuredevops-tools"]
