#!/bin/bash
consul agent -server -bootstrap-expect 1 -bind=172.16.18.6 -client=172.16.18.6 -data-dir=/opt/consul -node=agent-one -config-dir=/opt/consul/consul.d
