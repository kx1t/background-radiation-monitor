FROM ghcr.io/sdr-enthusiasts/docker-baseimage:base 

ARG TARGETARCH

COPY ./grafana.ini /usr/share/grafana/conf/custom.ini
COPY ./provisioning /usr/src/app/provisioning
COPY ./*.sh /usr/src/app/

RUN set -x && \
      chmod +x /usr/src/app/*.sh && \
      apt-get update -qq && apt-get install -y --no-install-recommends \
            fontconfig-config \
            fonts-dejavu-core \
            libfontconfig1 \
            ucf \
            jq \
            wget && \
      echo "Arch=${TARGETARCH}" && \
      /usr/src/app/download.sh "${TARGETARCH}" && \
      dpkg -i /tmp/grafana.deb && rm /tmp/grafana.deb && \
      # Clean-up
      apt-get remove -y ${TEMP_PACKAGES[@]} && \
      apt-get autoremove -y && \
      rm -rf /src/* /tmp/* /var/lib/apt/lists/*

CMD ["/bin/sh","/usr/src/app/entry.sh"]
