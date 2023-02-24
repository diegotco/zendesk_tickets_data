import logging
import sys

import config
import zd_ticket_messages

## Configure logging variables
logformat = "%(asctime)s %(levelname)s:%(name)s - %(message)s"
logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                format=logformat, datefmt="%Y-%m-%dT%H:%M:%S")

## Init of the script
logging.info("""
    <<Program started>>
    Please be patient. It's performing its tasks.
    You'll see a message when it's done.
    ////////////////////////////////////////////////////////////
""")

loaded_config = config.load_configuration()
zd_ticket_messages.load_zendesk_tickets(loaded_config)

# TODO modify logic inside this scripts
#import zd_ticket_messages, zd_split_messages, words, send_email

logging.info("""
    ////////////////////////////////////////////////////////////
    <<Program finished>>
""")
