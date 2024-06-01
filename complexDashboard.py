from grafanalib.core import (
    Dashboard, Graph, Row, TimeSeries, SingleStat, Target, YAxis, OPSFormat,
    GridPos, Table, TableColumn, TableStyle, Heatmap, GaugePanel, RepeatPanel
)

# Define a TimeSeries panel for CPU usage across multiple instances
cpu_graph = TimeSeries(
    title="CPU Usage",
    dataSource='Prometheus',
    targets=[
        Target(
            expr='avg(rate(node_cpu_seconds_total{mode!="idle"}[1m])) by (instance)',
            legendFormat="{{instance}}",
            refId='A',
        ),
    ],
    gridPos=GridPos(h=8, w=12, x=0, y=0),
    yAxes=[
        YAxis(format=OPSFormat.PERCENT_UNIT),
    ],
)

# Define a SingleStat panel for Memory Usage across instances
memory_singlestat = SingleStat(
    title="Memory Usage",
    dataSource='Prometheus',
    targets=[
        Target(
            expr='avg(node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)',
            refId='A',
        ),
    ],
    format=OPSFormat.PERCENT_UNIT,
    gridPos=GridPos(h=4, w=4, x=0, y=8),
)

# Define a Table panel for Disk I/O per instance
disk_io_table = Table(
    title="Disk I/O",
    dataSource='Prometheus',
    targets=[
        Target(
            expr='rate(node_disk_io_time_seconds_total[1m])',
            refId='A',
        ),
    ],
    gridPos=GridPos(h=8, w=12, x=12, y=0),
    styles=[
        TableStyle(
            type="number",
            pattern="Value",
            unit="short",
            decimals=2,
        ),
    ],
    columns=[
        TableColumn("Time", "time"),
        TableColumn("Instance", "string"),
        TableColumn("Value", "number"),
    ],
)

# Define a TimeSeries panel for Network Traffic
network_traffic_graph = TimeSeries(
    title="Network Traffic",
    dataSource='Prometheus',
    targets=[
        Target(
            expr='rate(node_network_receive_bytes_total[1m])',
            legendFormat="{{instance}} - Receive",
            refId='A',
        ),
        Target(
            expr='rate(node_network_transmit_bytes_total[1m])',
            legendFormat="{{instance}} - Transmit",
            refId='B',
        ),
    ],
    gridPos=GridPos(h=8, w=12, x=0, y=12),
    yAxes=[
        YAxis(format=OPSFormat.BYTES_PER_SEC),
    ],
)

# Define a Heatmap panel for CPU load
cpu_load_heatmap = Heatmap(
    title="CPU Load Heatmap",
    dataSource='Prometheus',
    targets=[
        Target(
            expr='histogram_quantile(0.99, sum(rate(node_cpu_seconds_total{mode!="idle"}[5m])) by (le, instance))',
            refId='A',
        ),
    ],
    gridPos=GridPos(h=8, w=12, x=12, y=12),
)

# Define a Gauge panel for System Load
system_load_gauge = GaugePanel(
    title="System Load",
    dataSource='Prometheus',
    targets=[
        Target(
            expr='avg(node_load1)',
            refId='A',
        ),
    ],
    gridPos=GridPos(h=4, w=4, x=4, y=8),
)

# Define a Row with repeated panels for per-instance metrics
per_instance_row = Row(
    title="Per-Instance Metrics",
    panels=[
        RepeatPanel(
            panel=TimeSeries(
                title="Instance CPU Usage",
                dataSource='Prometheus',
                targets=[
                    Target(
                        expr='rate(node_cpu_seconds_total{instance="$instance", mode!="idle"}[1m])',
                        legendFormat="{{cpu}} - {{mode}}",
                        refId='A',
                    ),
                ],
                yAxes=[
                    YAxis(format=OPSFormat.PERCENT_UNIT),
                ],
            ),
            repeat='instance',
        ),
    ],
)

# Define the dashboard with multiple rows and panels
dashboard = Dashboard(
    title="Advanced System Monitoring Dashboard",
    rows=[
        Row(
            title="System Overview",
            panels=[
                cpu_graph,
                memory_singlestat,
                disk_io_table,
                network_traffic_graph,
                cpu_load_heatmap,
                system_load_gauge,
            ],
        ),
        per_instance_row,
    ],
).auto_panel_ids()

# Generate the dashboard JSON and print it
print(dashboard.to_json_data())
