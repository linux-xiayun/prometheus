### 服务端 prometheus 部署
1.部署方式：采用 docker 安装  
2.部署的版本:目前用的是最新版本 v2.3.2  
3.部署的命令：

```
docker run -itd -p 9090:9090 --name prom_server -v /opt/prometheus.yml:/etc/prometheus/prometheus.yml 
                                                -v /opt/rules.yml:/etc/prometheus/rules.yml 
                                                -v /var/lib/prometheus:/var/lib/prometheus 
                                                prom/prometheus:v2.3.2
```  
### 告警服务 Alertmanager
* Prometheus 服务根据所设置的告警规则将告警信息发送给 Alertmanager
* Alertmanager 对收到的告警信息进行处理，包括去重，降噪，分组，策略路由告警通知

1.部署的方式：采用 docker 部署  
2.部署的版本： 使用最新版本 v0.15.0  
3.部署的命令： 
```
docker run -itd -p 9093:9093 -v /opt/alertmanager.yml:/etc/alertmanager/alertmanager.yml 
                             --name alertmanager prom/alertmanager:v0.15.0
```  

### Pushgateway 网关  
* 将多个节点数据汇总到 pushgateway, 如果 pushgateway 挂了，受影响比多个 target 大
* Prometheus 拉取状态 up 只针对 pushgateway, 无法做到对每个节点有效
* Pushgateway 可以持久化推送给它的所有监控数据 , 因此，即使你的监控已经下线，prometheus 还会拉取到旧的监控数据，需要手动清理 pushgateway 不要的数据。  

1.部署的方式：采用 docker 部署  
2.部署的版本：v0.5.2  
3.部署的命令：
```
docker run -itd -p 9091:9091 --name pushgateway prom/pushgateway:v0.5.2

```  

### Grafana  
1.部署的方式：采用 docker 部署  
2.部署的版本：5.2.1  
3.部署的命令：
```
docker run -itd -p 3000:3000 --name=grafana 
                             -v grafana-storage:/var/lib/grafana 
                             -e "GF_SECURITY_ADMIN_PASSWORD=zjl@204101011!" 
                             grafana/grafana:5.2.1
```  

### 钉钉报警通知  
```
nohup ./prometheus-webhook-dingtalk 
       --ding.profile="webhook1=https://oapi.dingtalk.com/robot/send?access_token=xxxx" &

```

### cadvisor
1.系统容器环境监控

### pg_prometheus && prometheus_postgresql_adapter
**remote_write/read**远端存储到第三方storage-timescale  
prometheus_postgresql_adapter提供prometheus<-->timescale的读写  
部署方式：**docker-compose**

### 采用 docker-compose 安装
