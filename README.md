# Monitoring Lab: Prometheus, Node Exporter, Grafana

Hands-on monitoring practice using Docker Compose.

## What is running
- **Prometheus** (port 9091 on host): collects and stores metrics
- **Node Exporter** (port 9100): gives host CPU, memory, disk and network metrics
- **Grafana** (port 3000): dashboards and alerts
- **demo-app** (port 8001): a Python app with its own `/metrics` (requests, errors, duration)

## Files
- `prometheus.yml`: scrape targets (prometheus, node, app) every 15s
- `rules.yml`: recording rule `instance:cpu_usage:percent`
- `docker-compose.yml`: runs all containers
- `Dockerfile` and `app.py`: the instrumented demo app

## Concepts learned
- Metrics vs logs vs traces
- Scraping, exporters, labels, time series, TSDB, retention (15 days by default)
- Metric types: counter, gauge, histogram, summary
- Cardinality: too many label values make Prometheus slow and heavy
- RED method (Rate, Errors, Duration) for services, USE method (Utilization, Saturation, Errors) for resources

## PromQL used
- CPU used %: `100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)`
- Memory used %: `100 - ((node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100)`
- Disk used %: `100 - (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"} * 100)`
- Network in: `rate(node_network_receive_bytes_total{device!="lo"}[1m])`
- Request rate: `rate(app_requests_total[1m])`
- Error %: `rate(app_errors_total[1m]) / rate(app_requests_total[1m]) * 100`
- p95 duration: `histogram_quantile(0.95, rate(app_request_duration_seconds_bucket[1m]))`

## Grafana
- Dashboard with CPU, Memory, Disk and Network panels
- Table panel "Target Status" using the `up` query and an Organize fields transformation
- Alert rule: disk usage above 85%

## Failed target test
Ran `docker stop node-exporter`, saw the `node` target go DOWN on `/targets` (`up` = 0), then `docker start node-exporter` brought it back UP.

## Issues fixed
- Ports 9090 and 8000 were already used on the host, so Prometheus uses 9091 and the app uses 8001 (container ports unchanged)
