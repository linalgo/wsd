ARG PY_VER
FROM asia.gcr.io/linalgo/wsd:vanilla-py${PY_VER}

ARG EXTRA

# Install the library
COPY dist/*.whl /tmp/wheels/
RUN uv pip install $(ls /tmp/wheels | sed 's|^|/tmp/wheels/|')[$EXTRA] --system && \
    sudo rm /tmp/wheels/*.whl
