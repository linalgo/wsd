ARG PY_VER
FROM asia.gcr.io/linalgo/wsd:vanilla-py${PY_VER}

ARG EXTRA

# Copy the project files
COPY pyproject.toml ./pyproject.toml
COPY .env ./.env
COPY README.md ./README.md
COPY wsd ./wsd

# Install the library
RUN pip install .[$EXTRA] --break-system-packages && rm -r pyproject.toml README.md .env wsd

ENTRYPOINT [ "bash" ]
