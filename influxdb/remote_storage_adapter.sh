go get -d -v github.com/prometheus/prometheus/documentation/examples/remote_storage/remote_storage_adapter  
go build -v github.com/prometheus/prometheus/documentation/examples/remote_storage/remote_storage_adapter
INFLUXDB_PW=xxx
nohup ./remote_storage_adapter -influxdb-url=http://localhost:8086 -influxdb.username=prom -influxdb.database=prometheus -influxdb.retention-policy=autogen -web.listen-address=:9301 &
