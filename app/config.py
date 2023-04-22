#
# Configuration of the application by reading a .env file or using the environment variables
#
import logging
import os
import sys

## Configure logging variables
logformat = "%(asctime)s %(levelname)s:%(name)s - %(message)s"
logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                format=logformat, datefmt="%Y-%m-%dT%H:%M:%S")

# Read initial configuration for the app
def load_configuration():
    logging.info('Loading configuration...')

    # Check if the configuration comes from a file
    ZENDESK_CONFIG = os.environ.get('ZENDESK_CONFIG')
    if ZENDESK_CONFIG is not None:
        return _read_config_from_file(ZENDESK_CONFIG)
    else:
        config = {}
        config['ZENDESK_USER'] = os.environ.get("ZENDESK_USER")
        config['ZENDESK_API_KEY'] = os.environ.get("ZENDESK_API_KEY")
        config['ZENDESK_OUTPUT_FILE'] = os.environ.get("ZENDESK_OUTPUT_FILE")
        logging.info("Username configured: " + config['ZENDESK_USER'])
        return config

## Read the configuration from a file
def _read_config_from_file(filename):
    config = {}
    with open(filename) as f:
        for line in f:
            key, value = line.strip().split("=")
            config[key] = value
    logging.info("Username configured from file: " + config['ZENDESK_USER'])
    return config