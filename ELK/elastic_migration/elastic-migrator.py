#!/usr/local/bin/python3

import migratorcfg	    # Also in this GitHub repo folder as migratorcfg.py
from migratorcfg import run_curl
from migratorcfg import create_curl_cmd
from elasticsearch import Elasticsearch
import json

KEEP_LOOPING = True
migratorcfg.DEBUGGING = False


source, dest = migratorcfg.slurp()
while KEEP_LOOPING:
    # Elastic only returns a handful or records at a time, so
    # keep looping through till they're exhausted
    es = Elasticsearch(
        [source["server"]],
        http_auth=(source["user"], source["password"]),
        scheme="http",
        port=source["port"]
    )
    # Query /INDEX/TYPE for all records
    results = es.search(index=source["index"], body={
        "query": {
            "bool": {
                "must": [
                    { "match": {"_type": source["type"]}}
                ]
            }
        }
    })
    migratorcfg.debug("Search params:", source["server"], source["port"], source["index"], source["type"])

    # es.search returns a dictionary, a lot of which I'm not currently
    # interested in. However I'm specifically interested in the "hits" field,
    # which is a pointer to another dictionary
    hits = results["hits"]
    migratorcfg.debug("Search matches:", hits["total"])
    if hits["total"] == 0:
        # No more hits, so break out of WHILE loop
        KEEP_LOOPING = False
    else:
        # The "hits" dictionary has a field which is also called "hits", which
        # in turn are a bunch of dictionaries; we want to loop through each of
        # those ...
        for rh in hits["hits"]:
            # The records we imported from github have a bunch of fields, plus 
            # a "sub-dictionary" of GitHub metadata
            record = dict(rh)["_source"]
            old_id = dict(rh)["_id"]
            payload = json.dumps(record, indent = 2)
            migratorcfg.debug("CREATING new record for:", old_id)
            try:
                cmd_output = run_curl(create_curl_cmd(dest, "write",\
                            payload=payload))
                migratorcfg.debug("Created record:", cmd_output)
                new_id = str(cmd_output).split("\"_id\":")[1].split("\"")[1]
                migratorcfg.debug("\tNEW ID:", new_id)
                try:
                    cmd_output = run_curl(create_curl_cmd(dest,"read", record=new_id))
                    cmd_output = run_curl(create_curl_cmd(source, "delete",\
                            record=old_id))
                except ValueError as e:
                    print("Cannot process old_id:", e, " - skipping")
            except ValueError as e:
                print("Cannot create new record for", old_id, ":", e)
                print(payload, "\n")
