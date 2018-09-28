# Prometheus
## 主要功能
- 多维 数据模型（时序由 metric 名字和 k/v 的 labels 构成）。
- 灵活的查询语句（PromQL）。
- 无依赖存储，支持 local 和 remote 不同模型。
- 采用 http 协议，使用 pull 模式，拉取数据，简单易懂。
- 监控目标，可以采用服务发现或静态配置的方式。
- 支持多种统计数据模型，图形化友好。
## 核心组件
- Prometheus Server， 主要用于抓取数据和存储时序数据，另外还提供查询和 Alert Rule 配置管理。
- client libraries，用于对接 Prometheus Server, 可以查询和上报数据。
- push gateway ，用于批量，短期的监控数据的汇总节点，主要用于业务数据汇报等。
- 各种汇报数据的 exporters ，例如汇报机器数据的 node_exporter, 汇报 MongoDB 信息的 MongoDB exporter 等等。
- 用于告警通知管理的 alertmanager 。
## 基础架构
![image](https://prometheus.io/assets/architecture.svg)
> 从这个架构图，也可以看出 Prometheus 的主要模块包含， Server, Exporters, Pushgateway, PromQL, Alertmanager, WebUI 等。

它大致使用逻辑是这样：
1. Prometheus server 定期从静态配置的 targets 或者服务发现的 targets 拉取数据。
2. 当新拉取的数据大于配置内存缓存区的时候，Prometheus 会将数据持久化到磁盘（如果使用 remote storage 将持久化到云端）。
3. Prometheus 可以配置 rules，然后定时查询数据，当条件触发的时候，会将 alert 推送到配置的 Alertmanager。
4. Alertmanager 收到警告的时候，可以根据配置，聚合，去重，降噪，最后发送警告。
5. 可以使用 API， Prometheus Console 或者 Grafana 查询和聚合数据。
## 注意
- Prometheus 的数据是基于时序的 float64 的值，如果你的数据值有更多类型，无法满足。
- Prometheus 不适合做审计计费，因为它的数据是按一定时间采集的，关注的更多是系统的运行瞬时状态以及趋势，即使有少量数据没有采集也能容忍，但是审计计费需要记录每个请求，并且数据长期存储，这个 Prometheus 无法满足，可能需要采用专门的审计系统。
## Docker安装Grafana

```
docker run -itd -p 3000:3000 --name=grafana \
-v grafana-storage:/var/lib/grafana \
-e "GF_SECURITY_ADMIN_PASSWORD=xiayun" \
grafana/grafana:5.2.1 \
```
### Dockerfile

```
FROM prom/prometheus
ADD prometheus.yml /etc/prometheus/
```

```
docker build -t my-prometheus .
docker run -p 9090:9090 my-prometheus
```
推荐将数据存储卷挂载到外部,以便当docker镜像升级时数据不丢失

## 配置文件在运行时动态reload
方式1：kill -HUP ${prometheus_pid}  
方式2：需要 --web.enable-lifecycle 参数为true  
curl -X POST http://10.0.209.140:9090/-/reload
## 配置文件
[以YAML格式编写：关于YAML格式的简单说明](http://www.jianshu.com/p/2583a81ebfd0)
### 配置文件内容
主要有以下几部分：
- global , 用于配置其他配置上下文中合法的参数,作为默认参数。
- rule_files, 用于设置规则文件所在位置(相对于当前工作目录)。
- scrape_configs: 用于设置多个不同的 scrape_config 对象。
- alerting: 用于设置alertmanager对象。
- remote_write 和 remote_read：与实验远程写入/读写特性相关的设置。
  
[配置文件示列](https://github.com/prometheus/prometheus/blob/master/config/testdata/conf.good.yml)  
## 配置rules
prometheus 支持两种类型的规则：
- 记录规则
- 警报规则  

如果想要在Prometheus中包含规则, 那就创建一个规则文件,其内容包含了必要的 rule statements,
然后通过Prometheus配置中的rule_files字段加载规则文件.
规则文件是 YAML 格式

在 Prometheus 运行时可以 reload rule files, 只需要给 Prometheus 进程发送 SIGHUP 信号.
当然只有在所有的规则文件都格式良好时才会成功.

要想快速检查规则文件是否存在语法错误,可以使用 Prometheus 提供的工具:
> go get github.com/prometheus/prometheus/cmd/promtool  
> promtool check-rules /path/to/example.rules
### rule files格式

```
groups:
  [ - <rule_group> ]
```
<rule_group> 格式:

```
name: <string>
[ interval: <duration> | default = global.evaluation_interval ]
rules:
  [ - <rule> ... ]
```
<rule> 格式:
recording <rule>的格式是:

```
record: <string>
expr: <string>
labels:
  [ <labelname>: <labelvalue> ]
```
alerting <rule>的格式是:

```
alert: <string>
expr: <string>
[ for: <duration> | default = 0s ]
labels:
  [ <labelname>: <tmpl_string> ]
annotations:
  [ <labelname>: <tmpl_string> ]
```
recording rules 例子 :

```
groups:
  - name: example
    rules:
    - record: job:http_inprogress_requests:sum
      expr: sum(http_inprogress_requests) by (job)
```
alerting rules 例子 :

```
groups:
- name: example
  rules:
  - alert: HighErrorRate
    expr: job:request_latency_seconds:mean5m{job="myjob"} > 0.5
    for: 10m
    labels:
      severity: page
    annotations:
      summary: High request latency
```
Recording rules 按照 evaluation_interval 字段设置的间隔定期 evaluated.
