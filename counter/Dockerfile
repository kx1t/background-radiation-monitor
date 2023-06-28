FROM ghcr.io/sdr-enthusiasts/docker-baseimage:python

WORKDIR /usr/app/src

RUN set -x && \
    TEMP_PACKAGES=() && \
    KEPT_PACKAGES=() && \
    TEMP_PACKAGES+=(gcc) && \
    TEMP_PACKAGES+=(build-essential) && \
    KEPT_PACKAGES+=(bash-builtins) && \
    KEPT_PACKAGES+=(python3-dev) && \
    # install packages
    apt-get update && \
    apt-get install -y --no-install-recommends \
        ${KEPT_PACKAGES[@]} \
        ${TEMP_PACKAGES[@]} \
        && \
    pip install wheel spidev RPi.GPIO influxdb && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1

COPY *.py ./

CMD ["python","counter.py"]
