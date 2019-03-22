#!/usr/local/bin/python3
# Migration script for copying GHE data from the POC ELK environment
# to the new Production cluster.


from datetime import datetime
from elasticsearch import Elasticsearch
import json
import os
import requests
import ssl
import sys


GKE_LOGSTASH_SERVER = "https://somelogstashserver.com"
GKE_LOGSTASH_CA_CERT = "./certauth.cert"
GKE_LOGSTASH_SSL_CERT = "./access.pem"

DEBUGGING = True
DEBUG_LEVEL = 4         # Valid values: 0..5

source = {
    "server"   : "poc-server.com",
    "port"     : "9200",
    "user"     : "user",
    "password" : "password",
    "index"    : "index",
    "type"     : "type"
}


def debug(value, *args):
    # Takes a string and prints it if DEBUGGING is on
    if DEBUGGING:
        if value <= DEBUG_LEVEL:
            print("DEBUG:", *args, "\n")


def export_from_poc() :
    records = []
    debug(1, "export_from_poc:", "starting loop:", str(datetime.now())
    # Elastic only returns a handful of records at a time, so
    # keep looping through till they're exhausted
    es = Elasticsearch(
        [source["server"]],
        http_auth=(source["user"], source["password"]),
        scheme="http",
        port=source["port"]
    )
    debug(1, "export_from_poc:", "Search params:", source["server"], source["port"], source["index"], source["type"])
    # Query /INDEX/TYPE for all records
    doc = {
        'size': 1000,
        'query': {
            'match_all': {}
        }
    }
    results = es.search(index=source["index"], doc_type=source["type"], body=doc, scroll='1m')
    debug(1, "export_from_poc:", "list-of-search-keys:", list(results.keys()))
    while results:
        # es.search returns a dictionary, a lot of which I'm not currently
        # interested in. However I'm specifically interested in the "hits" field,
        # which is a pointer to another dictionary
        hits = results["hits"]
        debug(2, "export_from_poc:", "number of hits:", hits["total"])
        if len(hits["hits"]) == 0:
            debug(3, "export_from_poc:", "finished processing hits")
            results = ""
        else:
            debug(3, "export_from_poc:", "processing next batch of hits")
            for rh in hits["hits"]:
                # The records we imported from github have a bunch of fields, 
                # plus a "sub-dictionary" of GitHub metadata
                record = dict(rh)["_source"]
                old_id = dict(rh)["_id"]
                records.append(record)
                debug(4, "export_from_poc:", "current #records:", len(records))
            scroll = results["_scroll_id"]
            results = es.scroll(scroll_id = scroll, scroll = '1m')
    debug(1, "export_from_poc:", "export complete:", str(datetime.now())    
    print(len(records), "total records exported")
    return records


def post_to_logstash(list_of_records):
    count = 0
    debug(1, "post_to_logstash:", "checking GHE server:", os.uname()[1])
    debug(1, "post_to_logstash:", "server =", GKE_LOGSTASH_SERVER)
    debug(1, "post_to_logstash:", "certificate path =", GKE_LOGSTASH_SSL_CERT)
    debug(1, "post_to_logstash:", "checking certificate exists ..", os.path.isfile(GKE_LOGSTASH_SSL_CERT))
    debug(1, "post_to_logstash:", "starting import:", str(datetime.now()))
    with requests.session() as elk_session:
        debug(2, "post_to_logstash:", "getting session:",
                "ssl_cert =", GKE_LOGSTASH_SSL_CERT, "ca_cert =", GKE_LOGSTASH_CA_CERT)
        debug(2, "\t-->", elk_session.get(GKE_LOGSTASH_SERVER, cert=GKE_LOGSTASH_SSL_CERT, verify=GKE_LOGSTASH_CA_CERT))
        elk_session.headers
        debug(2, "post_to_logstash:", "verifying session:")
        elk_session.verify = GKE_LOGSTASH_SSL_CERT
        for json_block in list_of_records:
            debug(5, "post_to_logstash:", "posting data:", GKE_LOGSTASH_SERVER, json_block)
            elk_session = requests.post(GKE_LOGSTASH_SERVER, json=json_block, cert=GKE_LOGSTASH_SSL_CERT, verify=GKE_LOGSTASH_CA_CERT)
            debug(5, "post_to_logstash:", "complete")
            count += 1
            if count % 1000 == 0 :
                debug(4, "post_to_logstash:", count, "records processed",
                    str(datetime.now()))
    debug(1, "post_to_logstash:", count, "TOTAL records processed")
    print(count, "records processed in total")

debug(0, "elastic-migrator.py")
post_to_logstash(export_from_poc())
sys.exit(0)

