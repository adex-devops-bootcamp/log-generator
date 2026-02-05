import json
import random
import time
import logging
import sys
from datetime import datetime
from logging.handlers import SocketHandler

LOGSTASH_HOST = "elk.tekbay.click"
LOGSTASH_PORT = 5044  # match your logstash tcp input

logger = logging.getLogger("demo-app")
logger.setLevel(logging.INFO)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "service": "demo-app",
            "message": record.getMessage(),
        })

formatter = JsonFormatter()

# 1️⃣ STDOUT (docker logs)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)

# 2️⃣ Logstash TCP handler
tcp_handler = SocketHandler(LOGSTASH_HOST, LOGSTASH_PORT)
logger.addHandler(tcp_handler)

# ---- App Loop ----
while True:
    level = random.choice(["INFO", "INFO", "ERROR"])
    action = random.choice(["login", "upload", "download"])

    if level == "ERROR":
        logger.error(f"Action failed: {action}")
    else:
        logger.info(f"Action success: {action}")

    time.sleep(5)
