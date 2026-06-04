# syntax=docker/dockerfile:1

# This file is a recipe for building the app into a single shippable image.
# It has TWO stages:
#   1. "builder"  - a temporary stage where we install the Python dependencies.
#   2. "runtime"  - the final, lean image we actually ship. It copies the installed
#                   dependencies out of the builder and throws the rest away.
# Splitting it this way keeps the final image small: build tools and caches stay
# behind in the builder and never end up in what we deploy.


# ============================================================
# Stage 1: builder - install the Python dependencies
# ============================================================
FROM python:3.12-slim AS builder

# `uv` is our Python package manager. Grab its program from uv's official image
# (pinned to version 0.8.11 so builds are reproducible).
COPY --from=ghcr.io/astral-sh/uv:0.8.11 /uv /uvx /bin/

# All following commands run inside /app.
WORKDIR /app

# A few settings that make uv behave well inside a container:
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0
# UV_COMPILE_BYTECODE=1  -> pre-compile Python files so the app starts a bit faster.
# UV_LINK_MODE=copy      -> copy package files instead of linking them (avoids warnings).
# UV_PYTHON_DOWNLOADS=0  -> use the Python already in this image; don't download another.

# Install ONLY the dependencies, before copying any of our own code.
# Why in this order: Docker remembers ("caches") each step. Dependencies change rarely,
# our code changes constantly. By installing dependencies first, editing our code later
# doesn't force a slow re-install every build - Docker reuses this cached step.
# --no-dev skips test/lint tools we don't need in production.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --no-install-project


# ============================================================
# Stage 2: runtime - the lean image we actually ship
# ============================================================
FROM python:3.12-slim AS runtime

# By default everything in a container runs as "root" - Linux's all-powerful admin
# account - which is risky if the app is ever compromised. So we create an ordinary,
# limited user named "appuser" and later switch to it (see USER below) to run the app.
# Reading the command:
#   useradd        -> the Linux command that creates a user account
#   --create-home  -> also give that user a home folder (/home/appuser)
#   --uid 1000     -> its id number (Linux tracks users by number; 1000 is the usual
#                     id for the first normal, non-system user)
#   appuser        -> the name we're giving the account
RUN useradd --create-home --uid 1000 appuser

WORKDIR /app

# Bring the installed dependencies over from the builder stage into this final image.
# Back in the builder, uv installed all the Python packages into a folder named
# /app/.venv (a "virtual environment" = this project's bundle of installed packages).
# We copy just that folder; the builder's caches and tools are left behind.
# Reading the command:
#   COPY                     -> copy files into the image
#   --from=builder           -> take them from the "builder" stage above, not from our
#                               project folder on disk
#   --chown=appuser:appuser  -> make "appuser" the owner of the copied files, so our
#                               limited user can use them (otherwise they'd be root's)
#   /app/.venv  /app/.venv   -> first path = source (in the builder), second = where to
#                               put it (in this image); same location in both
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv

# Copy only what the running app needs: our code (app/) and the prompt files it reads.
COPY --chown=appuser:appuser app/ ./app/
COPY --chown=appuser:appuser prompts/ ./prompts/

# Record which version of the code this image was built from. The build passes in the
# git commit id, and we save it so we can always tell exactly what's running.
ARG GIT_SHA=unknown
ENV GIT_SHA=${GIT_SHA}

# PATH: make the app use the dependencies we installed above.
# PYTHONUNBUFFERED=1: print logs immediately instead of holding them in a buffer, so we
# can actually see them in AWS's log viewer.
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

# Switch to the limited user, and note the app listens on port 8000.
USER appuser
EXPOSE 8000

# CMD is the default command Docker runs to start the container. Here it launches
# "uvicorn", the web server that runs our FastAPI app.
# Reading the arguments:
#   uvicorn         -> the web-server program
#   app.main:app    -> where our app lives: the object named "app" in app/main.py
#   --host 0.0.0.0  -> accept requests coming from outside the container (not just
#                      from inside it)
#   --port 8000     -> listen on port 8000
#
# Why it's a list ["uvicorn", ...] and not one plain string: the plain-string form
# would start uvicorn THROUGH a shell (an extra program in the middle). When AWS later
# tells the container to stop, that "please stop" signal would hit the shell instead of
# uvicorn, and the app could be killed abruptly. The list form runs uvicorn directly,
# so the stop signal reaches it and it can finish cleanly.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
