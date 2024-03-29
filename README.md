# Background Radiation Monitor

**A simple balenaCloud application to measure and record background radiation in your area. Radiation is detected with a cheaply available board, and connected to a Raspberry Pi to provide InfluxDB for datalogging and Grafana for pretty charts.**

![grafana-dashboard](https://raw.githubusercontent.com/balenalabs-incubator/background-radiation-monitor/master/assets/grafana-dashboard.png)

## Hardware required

* A Raspberry Pi 3B+ or later (4 or 5 will definitely work, but are a bit of overkill)
* A 32 GB (or larger) SD card (we recommend SanDisk Extreme Pro SD cards)
* A power supply (PSU)
* A radiation detector [Amazon UK](https://www.amazon.co.uk/KKmoon-Assembled-Counter-Radiation-Detector/dp/B07S86Q5X8) or [AliExpress](https://www.aliexpress.com/item/32884861168.html?spm=a2g0o.productlist.0.0.5faf6aa9OuQXsc)
* Some [Dupont cables/jumper jerky](https://shop.pimoroni.com/products/jumper-jerky?variant=348491271) (you’ll need 3 female-female cables - NOTE - check, they often come included with your radiation detector kit!)


## Hardware connection

There are 3 connections we need to make from the radiation detector board to the Raspberry Pi. They are +5V and Ground (GND) for power, and the output pulse line to detect the count. Note that this is called `Vin` which can be a bit confusing as this usually means ‘voltage input’ or something similar, but on this board, it’s the output.

![pi-geiger-simple](https://raw.githubusercontent.com/balenalabs-incubator/background-radiation-monitor/master/assets/pi-geiger-simple.png)

In this configuration you only need to provide 5 volt power to one of the two boards; if you’re powering the Pi with a standard micro-USB power supply, that will power the detector board via the connections we’ve just made, as well.

## Software setup

1. Get a Raspberry Pi and load a SD card image with Raspberry Pi OS or DietPi
2. Add this to end of `/boot/config.txt` to enable the GPIO headers:

```text
dtoverlay=vc4-kms-v3d
dtparam=i2c_arm=on
dtparam=spi=on
dtparam=audio=on
enable_uart=0
gpu_mem=16
```

3. Install Docker using the script from [this](https://github.com/sdr-enthusiasts/docker-install) page
4. Reboot your system and log in again
5. Enter the following commands:

```bash
sudo mkdir -p -m 777 /opt/geiger
cd /opt/geiger
wget 
docker compose up -d    # first time bringing the container up may take a while! 
```

Now you have a dashboard that can talk to an existing instance of Prometheus. Check that it works with:

```bash
docker logs -f counter
```

You can add the following to your `prometheus.yml` config file to ingest data (replace `1.2.3.4` with the IP of the machine on which your Geiger Counter is running):

```yaml
  - job_name: 'geiger'
    static_configs:
      - targets: ['1.2.3.4:9274']
```

If you want a sample Grafana dashboard, you can start with this one: [20075](https://grafana.com/grafana/dashboards/20075)

## Quick Reference

How-to.... 

* buy one of these: https://www.aliexpress.us/item/3256803888132442.html
hook 'm up like this: https://raw.githubusercontent.com/balenalabs-incubator/background-radiation-monitor/master/assets/pi-geiger-simple.png
* Clone this repo: https://github.com/kx1t/background-radiation-monitor
* add this to your /boot/config.txt and reboot your Raspberry Pi:

```text
dtoverlay=vc4-kms-v3d
dtparam=i2c_arm=on
dtparam=spi=on
dtparam=audio=on
enable_uart=0
gpu_mem=16
```

* do a docker compose up -d in the directory with docker-compose.yml
* Browse to your Raspberry Pi and it should be running!
Total cost (in addition to a Raspberry Pi) -- about $20