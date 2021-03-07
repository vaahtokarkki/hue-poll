import logging
import os
import sys
import time
from phue import Bridge

LOCK = False
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
        lights = bridge.get_light_objects('name')
        if lights[LIGHT_TO_POLL].on:
            time.sleep(TIMER)
            lights[LIGHT_TO_POLL].on = False
            logger.info(f'Turned off light {LIGHT_TO_POLL}')
    except Exception as e:
        logger.error("l", str(e))
    time.sleep(INTERVAL)
    LOCK = False

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
            logger.error("k", str(e))


if __name__ == "__main__":
    main()
