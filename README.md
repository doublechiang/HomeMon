# thermal_logging
recording the collect the temperature from sensor and saved in database, generate the plot

## Server Installation.
### Install RabbitMQ server
Rabbit MQ server default is for local access only.
[MacOS installed via brew bind local only](https://superuser.com/questions/464311/open-port-5672-tcp-for-access-to-rabbitmq-on-mac/516469#516469)

#### create rabbitmq server username/password for remote access.
Craete user by rabbitmqctl 

### Install Grafana
### setup InfluxDB
CREATE DATABASE thermal
brew install influxdb
$ brew services start influxdb # to start influxdb as service
$ INFLUXD_CONFIG_PATH=/usr/local/etc/influxdb2/config.yml influxd, to run as a process
$ influx setup, to configure the influx
$ influx org list, to show the configuration.

### To get weather
define the key in the environment
export WEATHER_APPKEY=[key]

### Use supervisord to daemonize the python program
easy_install supervisor

## Agent board
Raspberry board with thermal sensor DS18B20.
[Building Instruction on Raspberry](http://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/temperature/)

in /etc/modules
`w1-gpio
w1-therm`

Follow [DS18B20 not listed in /sys/bus/w1/devices](http://raspberrypi.stackexchange.com/questions/26623/ds18b20-not-listed-in-sys-bus-w1-devices)






