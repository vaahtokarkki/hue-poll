import logging
import os
import sys
import time
from phue import Bridge

LOCK, DIM_LOCK = False
BRIDGE_IP = os.environ.get('BRIDGE_IP')
LIGHT_TO_POLL = os.environ.get('LIGHT_TO_POLL')
TIMER = os.environ.get('TIMER', 5*60)
INTERVAL = os.environ.get('INTERVAL', 60)

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s',
                                datefmt='%d.%m.%y %H:%M')
console = logging.StreamHandler()
console.setFormatter(formatter)
logger.addHandler(console)

def get_bridge():
    config_path = f"{os.getcwd()}/.phue_config"
    return Bridge(BRIDGE_IP, config_file_path=config_path)

def poll(bridge, LIGHT_TO_POLL, LOCK):
    if LOCK:
        time.sleep(INTERVAL)
        return
    try:
        LOCK = True
        light_is_on = bridge.get_light(LIGHT_TO_POLL, 'on')
        if light_is_on:
            time.sleep(TIMER)
            bridge.set_light(LIGHT_TO_POLL, 'on', False)
            logger.info(f'Turned off light {LIGHT_TO_POLL}')
    except Exception as e:
        logger.exception(e)
    time.sleep(INTERVAL)
    LOCK = False

def dim(bridge, LIGHT_TO_DIM, DIM_LOCK):
    if DIM_LOCK:
        time.sleep(INTERVAL)
        return
    try:
        LOCK = True
        light = bridge.get_light(LIGHT_TO_DIM)
        if light.on and light.brightness > 60:
            time.sleep(TIMER)
            bridge.set_light(LIGHT_TO_POLL, 'bri', 60)
            logger.info(f'Dimmed light {LIGHT_TO_DIM}')
    except Exception as e:
        logger.exception(e)
    time.sleep(INTERVAL)
    DIM_LOCK = False

def main():
    if not BRIDGE_IP:
        logger.error('No bridge ip specified')
        exit()
    if not LIGHT_TO_POLL:
        logger.error('No light name specified')
        exit()

    bridge = get_bridge()
    logger.info(f'Hue poll started, connected to bridge {bridge.name}')
    while True:
        try:
            poll(bridge, LIGHT_TO_POLL, LOCK)
        except Exception as e:
            logger.exception(e)


if __name__ == "__main__":
    main()
