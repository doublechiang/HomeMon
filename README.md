# Home Monitoring

A Home Monitoring server, currently support read weather temperature local and thermostate temperature.

## Features
### Tempearture module
Show the historical temperature data in chart.
recording the collect the temperature from sensor and saved in database, generate the plot


## Development environemnt.
Install python3
$ pip3 install -r requirements.txt
$ export FLASK_APP=app.py (app.py is the default app, so it's not required to set this command.)
$ export FLASK_ENV=development

To run the server
$ python -m flask run

## Database setup.
Migrate from sqlite3 to postgres.
Database table name homemon


# Deployment

## Deploy to MAC
$ brew install supervisor

### Install RabbitMQ server
Rabbit MQ server default is for local access only.
[MacOS installed via brew bind local only](https://superuser.com/questions/464311/open-port-5672-tcp-for-access-to-rabbitmq-on-mac/516469#516469)

#### create rabbitmq server username/password for remote access.
Craete user by rabbitmqctl 

### To get weather
define the key in the environment
export WEATHER_APPKEY=[key]

### Use supervisord to daemonize the python program
pip3 install supervisor
$ supervisord -c ./supervisord.conf
To restart the supervisord
$ supervisorctl -c ./supervisord.conf reread
$ supervisorctl -c ./supervisord.conf update
$ supervisorctl -c ./supervisord.conf stop all
$ supervisorctl -c ./supervisord.conf start all


## Deployment to Heroku
$ heroku login
$ git push heroku master

### Configure the Heoku scheduler
$ heroku addons:open scheduler

### Configuration environment variable

$ heroku config:set WEATHER_APPKEY=....


## Agent board
Raspberry board with thermal sensor DS18B20.
[Building Instruction on Raspberry](http://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/temperature/)

in /etc/modules
`w1-gpio
w1-therm`

Follow [DS18B20 not listed in /sys/bus/w1/devices](http://raspberrypi.stackexchange.com/questions/26623/ds18b20-not-listed-in-sys-bus-w1-devices)


# Developemnt 
$ scp jiangjunyu@macmini:~/HomeMon/temperature.sqlite .



