# logger_config.py
import logging

# Create a logger with the desired configuration
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

log_handler = logging.StreamHandler()
log_handler.setFormatter(log_formatter)

log.addHandler(log_handler)