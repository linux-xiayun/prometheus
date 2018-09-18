有2种方式可以获取 node_exporter 的监控数据  

1.服务端主动去客户端拉取  
2.如果没有公网地址，客户端可以主动向pushgateway上传  
可以用 crontab 去每隔一段时间上传数据  
*/1 * * * * curl -s http://localhost:9100/metrics | curl --data-binary @- http://pushgateway:9091/metrics/job/pushgateway/instance/000e_c4d5_0a45
