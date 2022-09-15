FROM       python:3.9
RUN        pip install ascend-io-sdk
COPY       . /app
WORKDIR    /app
ENV        SHELL=/bin/bash
ENTRYPOINT python upload.py

