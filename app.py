import json
import random
import time
import logging
import sys
import os
from datetime import datetime
from logging.handlers import SocketHandler
import watchtower
import boto3

# ---- ENV VARS ----
LOGSTASH_HOST = os.getenv("LOGSTASH_HOST")
LOGSTASH_PORT = int(os.getenv("LOGSTASH_PORT", 0))
AWS_REGION = os.getenv("AWS_REGION")
LOG_GROUP = os.getenv("CW_LOG_GROUP")
LOG_STREAM = os.getenv("CW_LOG_STREAM")

# ---- Logger Setup ----
logger = logging.getLogger("demo-app")
logger.setLevel(logging.INFO)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "service": "demo-app",
            "message": record.getMessage()
        })

formatter = JsonFormatter()

# 1️⃣ STDOUT (docker logs)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)

# 2️⃣ Logstash TCP (only if provided)
if LOGSTASH_HOST and LOGSTASH_PORT:
    tcp_handler = SocketHandler(LOGSTASH_HOST, LOGSTASH_PORT)
    logger.addHandler(tcp_handler)

# 3️⃣ CloudWatch (only if provided)
if AWS_REGION and LOG_GROUP:
    boto3_client = boto3.client("logs", region_name=AWS_REGION)
    cw_handler = watchtower.CloudWatchLogHandler(
        boto3_client=boto3_client,
        log_group=LOG_GROUP,
        stream_name=LOG_STREAM or "app-stream"
    )
    cw_handler.setFormatter(formatter)
    logger.addHandler(cw_handler)

# ---- App Loop ----
while True:
    level = random.choice(["INFO", "INFO", "ERROR"])
    action = random.choice(["login", "upload", "download"])

    if level == "ERROR":
        logger.error(f"Action failed: {action}")
    else:
        logger.info(f"Action success: {action}")

    time.sleep(1)
