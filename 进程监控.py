#!/usr/bin/python
import os
import time
bootstrap_jar = "/home/admin/localserver/tomcat/bin/bootstrap.jar"
pid_name = "java_pid"
pid_status = ""

while True:
    time.sleep(60)
    pid_list = os.popen("ps aux |grep %s | grep -v grep | awk '{print $2}' "%bootstrap_jar).read().strip('\r\n').strip('').split('\n')
    if pid_list == ['']:
        pid_status = 1
        os.system("echo %s %s | curl --data-binary @- http://116.62.164.228:9091/metrics/job/pushgateway/instance/14b3-1f2d-0f42" % (pid_name,pid_status))
    else:
        print(pid_status)
        os.system("echo %s %s | curl --data-binary @- http://116.62.164.228:9091/metrics/job/pushgateway/instance/14b3-1f2d-0f42" % (pid_name, pid_status))
