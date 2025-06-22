import logging
import json
import sys

class JSONLFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'level': record.levelname,
            'message': record.getMessage(),
            'name': record.name,
            'time': self.formatTime(record, self.datefmt),
        }
        return json.dumps(log_record)

def setup_jsonl_logger(log_file=None, level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout) if log_file is None else logging.FileHandler(log_file)
    handler.setFormatter(JSONLFormatter())
    logger.handlers = [handler]
    return logger
