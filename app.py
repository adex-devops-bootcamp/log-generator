import json
import random
import time
from datetime import datetime
import sys

while True:
    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": random.choice(["INFO", "INFO", "ERROR"]),
        "service": "demo-app",
        "user_id": random.randint(1, 10),
        "action": random.choice(["login", "upload", "download"])
    }

    sys.stdout.write(json.dumps(log) + "\n")
    sys.stdout.flush()

    time.sleep(5)
