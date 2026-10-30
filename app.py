from prometheus_client import start_http_server, Counter, Histogram
import random
import time

REQUESTS = Counter("app_requests_total", "Total requests handled")
ERRORS = Counter("app_errors_total", "Total failed requests")
DURATION = Histogram("app_request_duration_seconds", "Time taken per request")

start_http_server(8000)

while True:
    with DURATION.time():
        time.sleep(random.uniform(0.1, 1.0))
    REQUESTS.inc()
    if random.random() < 0.1:
        ERRORS.inc()
