import logging
import sys

from config import FLASK_HOST, FLASK_PORT
from server.flask_forwarding import APP


def _setup_logging():
    log_format = logging.Formatter(fmt='[%(asctime)s][%(module)s][%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger('')
    logger.setLevel(logging.INFO)

    file_log = logging.FileHandler('/tmp/server.log')
    file_log.setLevel(logging.DEBUG)
    file_log.setFormatter(log_format)
    logger.addHandler(file_log)

    console_log = logging.StreamHandler()
    console_log.setFormatter(log_format)
    logger.addHandler(console_log)


def main():
    _setup_logging()
    try:
        APP.run(host=FLASK_HOST, port=FLASK_PORT, ssl_context='adhoc')
    except KeyboardInterrupt:
        logging.info('Bye, bye ..')


if __name__ == '__main__':
    sys.exit(main())
