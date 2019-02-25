#!/usr/bin/python
import os,sys
import time
import getopt


def usage():
    print("""Usage: check_http_status [-h|--help] [-s|--service service] [-p|--pid pid_name] [-j|--job job_name]
"
Url: the url that you want to check;
String: the string that you want to match;
"
For example,#python client.py -s localserver -p java -j tx-java-alived 
""")
    sys.exit(3)



def get_ip():
    out = os.popen("ifconfig |grep -A 1 eth0|grep inet|awk '{print $2}'").read().strip('\n').strip('')
    return out

def push_metrics(pid_name, job_name, instance_name):
    pid_list = os.popen("ps aux |grep %s | grep -v grep | awk '{print $2}' " % bootstrap_jar).read().strip('\r\n').strip('').split('\n')
    if pid_list:
        pid_status = 1
        os.system("echo %s %s | curl --data-binary @- http://120.27.220.136:9091/metrics/job/%s/instance/%s" % (pid_name, pid_status, job_name, instance_name))
    else:
        pid_status = 0
        os.system("echo %s %s | curl --data-binary @- http://120.27.220.136:9091/metrics/job/%s/instance/%s" % (pid_name, pid_status, job_name, instance_name))

if __name__ == "__main__":
    pid_status = ""
    instance_name = get_ip()
    try:
        options, args = getopt.getopt(sys.argv[1:],
                                      "hs:p:j:",
                                      "--help --service= --pid= --job=",
                                      )
    except getopt.GetoptError:
        usage()
        sys.exit(3)

    for name, value in options:
        if name in ("-h", "--help"):
            usage()
        if name in ("-s", "--service"):
            global service,bootstrap_jar
            service = value
            bootstrap_jar = "/home/admin/%s/tomcat/bin/bootstrap.jar" % service
        if name in ("-p", "--pid"):
            global pid_name
            pid_name = value
        if name in ("-j", "--job"):
            global job_name
            job_name = value
    print(bootstrap_jar,pid_name,job_name)
    push_metrics(pid_name, job_name, instance_name)
