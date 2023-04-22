import logging
import sys

import config
import write_output
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
output_filename = config("ZENDESK_OUTPUT_FILE")

# Read tickets from Zendesk and write the result into a file
ticket_descriptions = zd_ticket_messages.read_zendesk_tickets(loaded_config)
write_output.write_to_file(output_filename, ticket_descriptions)

# TODO modify logic inside this scripts
#import zd_ticket_messages, zd_split_messages, words, send_email

logging.info("""
    ////////////////////////////////////////////////////////////
    <<Program finished>>
""")
