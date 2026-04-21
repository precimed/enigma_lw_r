FROM quay.io/condaforge/miniforge3:26.1.1-3

ENV TZ=Europe
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /tmp
COPY /scripts/environment.yml .
RUN mamba env update --name base --file environment.yml && \
    conda clean --all --yes && \
    rm -rf /tmp/*

WORKDIR /home
