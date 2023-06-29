FROM ghcr.io/sdr-enthusiasts/docker-baseimage:python

RUN set -x && \
    TEMP_PACKAGES=() && \
    KEPT_PACKAGES=() && \
    TEMP_PACKAGES+=(gcc) && \
    TEMP_PACKAGES+=(build-essential) && \
    TEMP_PACKAGES+=(git) && \
    KEPT_PACKAGES+=(bash-builtins) && \
    KEPT_PACKAGES+=(python3-dev) && \
    KEPT_PACKAGES+=(nano) && \
    #
    # install packages
    apt-get update && \
    apt-get install -y --no-install-recommends \
        ${KEPT_PACKAGES[@]} \
        ${TEMP_PACKAGES[@]} \
        && \
    pip install wheel spidev RPi.GPIO influxdb && \
    #
    # Add Container Version
    branch="##BRANCH##" && \
    [[ "${branch:0:1}" == "#" ]] && branch="main" || true && \
    git clone --depth=1 -b $branch https://github.com/sdr-enthusiasts/docker-tar1090.git /tmp/clone && \
    pushd /tmp/clone && \
    bash -ec 'echo "$(TZ=UTC date +%Y%m%d-%H%M%S)_$(git rev-parse --short HEAD)_$(git branch --show-current)" > /.CONTAINER_VERSION' && \
    popd && \
    #
    # Clean-up
    apt-get remove -y ${TEMP_PACKAGES[@]} && \
    apt-get autoremove -y && \
    rm -rf /src/* /tmp/* /var/lib/apt/lists/*

COPY rootfs/ /

#CMD ["python","counter.py"]
