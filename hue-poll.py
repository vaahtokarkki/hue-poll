import logging
import os
import sys
import time
from phue import Bridge

LOCK = {"dim": 0, "off": 0}
BRIDGE_IP = os.environ.get('BRIDGE_IP')
LIGHT_TO_POLL = os.environ.get('LIGHT_TO_POLL')
LIGHT_TO_DIM = os.environ.get('LIGHT_TO_DIM')
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

def turn_off(bridge, LIGHT_TO_POLL):
    try:
        bridge.set_light(LIGHT_TO_POLL, 'on', False)
        logger.info(f'Turned off {LIGHT_TO_POLL}')
        return True
    except Exception as e:
        logger.exception(e)
    return False

def poll(bridge, LIGHT_TO_POLL):
    if LOCK['off'] == 5:
        turn_off(bridge, LIGHT_TO_POLL)
        LOCK['off'] = 0
    elif LOCK['off'] > 0:
        LOCK['off'] += 1
    else:
        light_is_on = bridge.get_light(LIGHT_TO_POLL, 'on')
        if light_is_on:
            LOCK['off'] = 1

def dim(bridge, LIGHT_TO_DIM):
    light_is_on = bridge.get_light(LIGHT_TO_DIM, 'on')
    if not light_is_on:
        logger.info(f'Light is already off')
        return False
    try:
        bridge.set_light(LIGHT_TO_DIM, 'bri', 60)
        logger.info(f'Dimmed light {LIGHT_TO_DIM}')
        return True
    except Exception as e:
        logger.exception(e)
    return False

def dim_poll(bridge, LIGHT_TO_DIM):
    if LOCK['dim'] == 2:
        dim(bridge, LIGHT_TO_DIM)
        LOCK['dim'] = 0
    elif LOCK['dim'] > 0:
        LOCK['dim'] += 1
    else:
        light_is_on = bridge.get_light(LIGHT_TO_DIM, 'on')
        light_bri = bridge.get_light(LIGHT_TO_DIM, 'bri')
        if light_is_on and light_bri > 60:
            LOCK['dim'] = 1


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
            poll(bridge, LIGHT_TO_POLL)
            dim_poll(bridge, LIGHT_TO_DIM)
        except Exception as e:
            logger.exception(e)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
