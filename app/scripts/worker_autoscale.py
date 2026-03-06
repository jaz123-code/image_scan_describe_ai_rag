import subprocess
import redis
import time

r=redis.Redis(host="redis", port=6379)

MIN_WORKERS=1
MAX_WORKERS=6

while True:
    queue_length=r.llen("celery")

    if queue_length<5:
        target=1
    elif queue_length<20:
        target=3
    else:
        target=6

    subprocess.run(
        ["docker", "compose", "up", "--scale", f"worker={target}", "--d"]
    )
    time.sleep(5)
    