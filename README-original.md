# Background Radiation Monitor

A simple application to measure background radiation in your area using a cheaply available board and a Raspberry Pi. The output is available in InfluxDB and Prometheus format, and can be displayed on a Grafana dashboard.

This project is a modified fork of [https://github.com/chrisys/background-radiation-monitor](https://github.com/chrisys/background-radiation-monitor). Whereas the original project created a Balena SD card image that was fully remotely manageable through the Balena Cloud, we created a simple Docker container that can output data in Influxdb or Prometheus format.

## Hardware required

* A Raspberry Pi (any model should be good for this, but I’d recommend a 3 or above just for performance reasons)
* Linux OS installed on the SD card. If you start from scratch, we recommend [DietPi](https://dietpi.com)
* A power supply (PSU)
* A cheap radiation detector, for example [this one on AliExpress](https://www.aliexpress.com/item/32884861168.html?spm=a2g0o.productlist.0.0.5faf6aa9OuQXsc)

## Hardware connection

There are 3 connections we need to make from the radiation detector board to the Raspberry Pi. They are +5V and Ground (GND) for power, and the output pulse line to detect the count. Note that this is called `VIN` which can be a bit confusing as this usually means ‘voltage input’ or something similar, but on this board, it’s the output.

![pi-geiger-simple](https://raw.githubusercontent.com/balenalabs-incubator/background-radiation-monitor/master/assets/pi-geiger-simple.png)

In this configuration you only need to provide 5 volt power to one of the two boards; if you’re powering the Pi with a standard micro-USB/USB-C power supply, that will power the detector board via the connections we’ve just made, as well.

## Software setup

* On your Raspberry Pi, make sure that the GPIO pins and SpiDev are enabled. You can do that by issuing this command, and then reboot your Pi:

```bash
cat << EOF | sudo tee -a testfile.txt >/dev/null
dtoverlay=vc4-kms-v3d
dtparam=i2c_arm=on
dtparam=spi=on
dtparam=audio=on
enable_uart=0
gpu_mem=16
EOF
```

* You need to have Docker installed. If you don't, please follow the instruction on [this page](https://github.com/sdr-enthusiasts/docker-install).
* Install the project. This can be done easily with these commands:

```bash
sudo mkdir -m 777 -p /opt/geiger
git clone https://github.com/kx1t/background-radiation-monitor.git /opt/geiger
```

* Now you can start the software. By default, 

## Access the dashboard

Once the software has been deployed and downloaded to your device, the dashboard will be accessible on the local IP address of the device, or via the balenaCloud public URL feature.

![public-url](https://raw.githubusercontent.com/balenalabs-incubator/background-radiation-monitor/master/assets/public-url.png)
