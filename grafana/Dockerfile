FROM ghcr.io/sdr-enthusiasts/docker-baseimage:base 

COPY ./grafana.ini /usr/share/grafana/conf/custom.ini
COPY ./provisioning /usr/src/app/provisioning
COPY ./*.sh /usr/src/app/
RUN chmod +x /usr/src/app/*.sh

RUN apt-get update -qq && apt-get install -y --no-install-recommends \
      fontconfig-config \
      fonts-dejavu-core \
      libfontconfig1 \
      ucf \
      jq \
      wget

RUN /usr/src/app/download.sh aarch64

RUN dpkg -i /tmp/grafana.deb && rm /tmp/grafana.deb

CMD ["/bin/sh","/usr/src/app/entry.sh"]
