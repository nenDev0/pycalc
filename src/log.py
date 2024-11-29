import logging

log = logging.Logger("log")
log.setLevel(logging.ERROR)
log_handler = logging.StreamHandler()
log.addHandler(log_handler)