import logging
import sys

## Configure logging variables
logformat = "%(asctime)s %(levelname)s:%(name)s - %(message)s"
logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                format=logformat, datefmt="%Y-%m-%dT%H:%M:%S")

WRITE_MODE = 'w'

# Write a file with the specified content. If something goes wrong, print the
# error on log and finish
def write_to_file(filename, content):

    try:
        logging.info('Writing results into file: ', filename)
        with open(filename, WRITE_MODE) as f:
            f.write(str(content))
        logging.info('Finished to write content into file ', filename)
    except IOError as err:
        logging.error("An error occurred while writing to the file", err)