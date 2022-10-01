Mega simple hue script to turn off light when it is turned on.

# [deprecated] hue-poll

Create file `.env` and add following content:
```
BRIDGE_IP=192.168.x.x
LIGHT_TO_POLL=
TIMER=
```

Light to poll contains the name of the light to turn off when turned on. By default interval to check light status is 1 minute and can be changed with `INTERVAL` (seconds) env variable. The light is turned off after 5 minutes when detected to be on, this can be adjusted as well with env variable `TIMER` (seconds).

Run on RPi Zero with Docker and docker-compose by copying the `docker-compose.yml` to your RPi and:

```
touch .phue_config
docker-compose up -d hue-poll-armv6
```
