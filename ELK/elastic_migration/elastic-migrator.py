#!/usr/local/bin/python3
# Migration script for copying GHE data from the POC ELK environment
# to the new Production cluster. This will connect to the POC and download
# all records into a list (be careful if your POC has a ton of data!!); then
# it connects to the new logstash server and uploads them all.
#
# WARNING: for large datasets, you'll want to modify the script so that
# export_from_poc() calls post_to_logstash() every time it's grabbed 1000
# records; it'll run more slowly but is unlikely to run out of memory.


from datetime import datetime
from elasticsearch import Elasticsearch
import json
import os
import requests
import ssl
import sys


GKE_LOGSTASH_SERVER = "https://somelogstashserver.com"
GKE_LOGSTASH_CA_CERT = "./cert-authority.cert"
GKE_LOGSTASH_SSL_CERT = "./UserCertPlusRSA.pem"

DEBUGGING = True
DEBUG_LEVEL = 4         # Valid values are currently 0..5

source = {      # POC details
    "server"   : "oldPOCserver.com",
    "port"     : "9200",
    "user"     : "user",
    "password" : "secretpassword",
    "index"    : "ourindex",
    "type"     : "ourtype"
}


def debug(value, *args):
    # Takes a string and prints it if DEBUGGING is on
    if DEBUGGING:
        if value <= DEBUG_LEVEL:
            print("DEBUG:", *args, "\n")


def export_from_poc() :
    records = []
    debug(1, "export_from_poc:", "starting loop:", str(datetime.now())
    es = Elasticsearch(
        [source["server"]],
        http_auth=(source["user"], source["password"]),
        scheme="http",
        port=source["port"]
    )       # Connects to elasticsearch server
    debug(1, "export_from_poc:", "Search params:", source["server"], source["port"], source["index"], source["type"])
    # Set things up to grab 1000 records at a time
    doc = {
        'size': 1000,
        'query': {
            'match_all': {}
        }
    }
    # Now run the search; 'scroll=' should be higher than the number of records
    # so you can collect them all
    results = es.search(index=source["index"], doc_type=source["type"], body=doc, scroll='1m')
    debug(1, "export_from_poc:", "list-of-search-keys:", list(results.keys()))
    while results:
        # es.search returns a dictionary, a lot of which I'm not currently
        # interested in. However I'm specifically interested in the "hits" 
        # field, which is a pointer to another dictionary
        hits = results["hits"]
        debug(2, "export_from_poc:", "number of hits:", hits["total"])
        if len(hits["hits"]) == 0:  # No more hits; we can stop
            debug(3, "export_from_poc:", "finished processing hits")
            results = ""
        else:       # Still collecting data so keep processing
            debug(3, "export_from_poc:", "processing next batch of hits")
            for rh in hits["hits"]:
                # The records we imported from github have a bunch of fields, 
                # plus a "sub-dictionary" of GitHub metadata
                record = dict(rh)["_source"]
                old_id = dict(rh)["_id"]
                debug(5, "export_from_poc:", "POC original ID:", old_id)
                records.append(record)
                debug(5, "export_from_poc:", "current #records:", len(records))
            scroll = results["_scroll_id"]  # This is the ID of the next
                    # record that has yet to be downloaded, so that ...
            results = es.scroll(scroll_id = scroll, scroll = '1m')
                    # ... starts collecting again at that record ID
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
    # Open a connection to logstash
    with requests.session() as elk_session:
        debug(2, "post_to_logstash:", "getting session:",
                "ssl_cert =", GKE_LOGSTASH_SSL_CERT, "ca_cert =", GKE_LOGSTASH_CA_CERT)
        debug(2, "\t-->", elk_session.get(GKE_LOGSTASH_SERVER, cert=GKE_LOGSTASH_SSL_CERT, verify=GKE_LOGSTASH_CA_CERT))
        elk_session.headers
        debug(2, "post_to_logstash:", "verifying session:")
        elk_session.verify = GKE_LOGSTASH_SSL_CERT
        # Start importing records
        for json_block in list_of_records:
            debug(5, "post_to_logstash:", "posting data:", GKE_LOGSTASH_SERVER, json_block)
            elk_session = requests.post(GKE_LOGSTASH_SERVER, json=json_block, cert=GKE_LOGSTASH_SSL_CERT, verify=GKE_LOGSTASH_CA_CERT)
            debug(5, "post_to_logstash:", "complete")
            # I find it useful to be able to keep an eye on how the script is
            # running - this'll just print an update every 1000 records, or
            # about 2mins on our setup
            count += 1
            if count % 1000 == 0 :
                debug(4, "post_to_logstash:", count, "records processed",
                    str(datetime.now()))
    debug(1, "post_to_logstash:", count, "TOTAL records processed")
    print(count, "records processed in total")

debug(0, "elastic-migrator.py")
post_to_logstash(export_from_poc())
sys.exit(0)

