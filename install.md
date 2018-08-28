官网：https://prometheus.io/  
GitHub：https://github.com/prometheus  
最新release版本下载地址：https://github.com/prometheus/prometheus/releases  
官方Docker Image下载地址:https://hub.docker.com/u/prom/

### 服务端 prometheus 部署
1.部署方式：采用 docker 安装  
2.部署的版本:目前用的是最新版本 v2.3.2  
3.部署的命令：

```
docker run -itd -p 9090:9090 --name prom_server -v /opt/prometheus.yml:/etc/prometheus/prometheus.yml 
                                                -v /opt/rules.yml:/etc/prometheus/rules.yml 
                                                -v /var/lib/prometheus:/var/lib/prometheus prom/prometheus:v2.3.2
```
