#!/usr/bin/env python3

import json
import os
import subprocess
import sys
import datetime
import socket

ELASTIC_ADDR = "www.my_ELK_host.com:9200"     # GMS:TODO:
ELASTIC_USER = "user:password"
ELASTIC_RECORD = "/index/type/"     # for importing data into Elastic
ELASTIC_TESTING = "/testing/type/"    # for local testing
MY_DEBUG = False	# Switch to true for debugging output

def get_ip() :
    # Returns the user's workstation IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def organise_data () :
    # No idea what kind of data we'll get, so stage 1 is to just record everything we get
    testing = False
    data_out = {}
    for entry in os.environ :
        data_out[entry] = os.getenv(entry)
    # Is this script being run for testing purposes, or from the BASTION host?
    # If it's local testing, write to a testing database instead
    if "ITERM_PROFILE" in data_out :
        testing = True
    # Additional info that github doesn't provide as an 
    # environment variable
    now = datetime.datetime.now()
    data_out["date"], data_out["time"] = str(now).split()
    data_out["ip_address"] = get_ip()
    return testing, json.dumps(data_out, indent = 2)

def send_to_elasticsearch () :
    # Wraps everything in curl command, which is then 
    # executed to transmit the data to elasticsearch
    global ELASTIC_RECORD, ELASTIC_TESTING
    testing, data = organise_data()
    if testing :
        # We're running locally so use the test database instead
        ELASTIC_RECORD = ELASTIC_TESTING
    payload = "'\n" + data + "'"
    cmdcurl = "curl -u " + ELASTIC_USER + " -POST " \
            + ELASTIC_ADDR + ELASTIC_RECORD \
            + " -curl -H 'Content-Type: application/json' -d " + payload
    cmd_output = subprocess.run(cmdcurl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if MY_DEBUG :
        if "testing" in ELASTIC_RECORD :
            print("TESTING LOCALLY")
        print("\nPAYLOAD:\n", payload)
        print("\nCMDCURL\n----\n", cmdcurl, "===========\n")
        print("\n----\nOS.SYSTEM\n", os.system(cmdcurl))
        if "Connection reset" in str(cmd_output.stderr) :
            # stderr has contents even on success, so can't
            # just check if it exists
            print("Pre-receive Hook Error: Cannot transmit to Elasticsearch")
            print(cmd_output.stderr)
            print("E-mail output to: garry.short@ikea.com")
        if len(cmd_output.stdout) > 0 : # Transmit succeeded
            print("SUCCESS: \n", cmd_output.stdout, "\n.. COMPLETE")


send_to_elasticsearch()
sys.exit(0)

