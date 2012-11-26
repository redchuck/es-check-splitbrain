#! /usr/bin/python

import os, time, json, string, sys, jsonpath, jsonlib, urllib, re

ip=sys.argv[1]

url="http://"+ ip + ":9200/_cluster/state?filter_routing_table=true&filter_blocks=true&filter_indices=true"

result=json.load(urllib.urlopen(url))

master_node=jsonpath.jsonpath(result, "master_node")
#print("%s master: %s" % ( ip, master_node ) )

for node in jsonpath.jsonpath(result, "nodes.*"):
  name = node["name"]
  url="http://"+ name + ":9200/_cluster/state?filter_routing_table=true&filter_blocks=true&filter_indices=true"
  memberresult=json.load(urllib.urlopen(url))
  membermaster_node=jsonpath.jsonpath(memberresult, "master_node")
  #print("%s master: %s" % ( name, membermaster_node ) )
  if membermaster_node != master_node:
    print("[CRITICAL] Master node mismatch on %s" % ( ip ) )
    sys.exit(2)

print("[OK] Masters all match")
sys.exit(0)
