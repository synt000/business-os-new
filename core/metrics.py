from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "business_os_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "business_os_request_latency_seconds",
    "Request latency"
)
