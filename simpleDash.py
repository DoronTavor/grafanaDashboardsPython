from grafanalib.core import (
    Dashboard, Graph, Row, TimeSeries, SingleStat, Target, YAxis, OPSFormat,
    GridPos, Table, TableColumn, TableStyle, TablePanel
)

# Define a Graph panel for CPU usage
cpu_graph = TimeSeries(
    title="CPU Usage",
    dataSource='Prometheus',
    targets=[
        Target(
            expr='rate(node_cpu_seconds_total{mode!="idle"}[1m])',
            legendFormat="{{cpu}} - {{mode}}",
            refId='A',
        ),
    ],
    gridPos=GridPos(h=8, w=12, x=0, y=0),
    yAxes=[
        YAxis(format=OPSFormat.PERCENT_UNIT),
    ],
)

# Define a SingleStat panel for Memory Usage
memory_singlestat = SingleStat(
    title="Memory Usage",
    dataSource='Prometheus',
    targets=[
        Target(
            expr='node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes',
            refId='A',
        ),
    ],
    format=OPSFormat.PERCENT_UNIT,
    gridPos=GridPos(h=4, w=4, x=0, y=8),
)

# Define a Table panel for Disk I/O
disk_io_table = TablePanel(
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

# Define a Graph panel for Network Traffic
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

# Create a row containing all the panels
main_row = Row(
    title="Main Row",
    panels=[
        cpu_graph,
        memory_singlestat,
        disk_io_table,
        network_traffic_graph,
    ],
)

# Define the dashboard
dashboard = Dashboard(
    title="System Overview Dashboard",
    rows=[
        main_row,
    ],
).auto_panel_ids()

# Generate the dashboard JSON and print it
print(dashboard.to_json_data())
