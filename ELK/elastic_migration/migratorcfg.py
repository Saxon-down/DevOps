#!/usr/local/bin/python3
# This is intended to be used as a module, for use with my
# ELK-based scripts

import json
import subprocess

MIGRATION_CONFIG = "elastic-migrator.cfg"
DEBUGGING = False

def debug(*args):
    # Takes a string and prints it if DEBUGGING is on
    if DEBUGGING:
        print("DEBUG:", *args, "\n")


def slurp() -> "separate dicts for source and dest" :
    '''
    Imports configuration details from elastic-migrator.cfg and
    splits it into two dictionaries, which it returns as SOURCE and 
    DEST
    '''
    with open(MIGRATION_CONFIG) as f:
        data = json.load(f)
    debug("migratorcfg.slurp:source =\n", json.dumps(data["source"], indent=2))
    debug("migratorcfg.slurp:dest =\n", json.dumps(data["destination"], \
            indent=2))
    return data["source"], data["destination"]


def create_curl_cmd(server_dict: "dict of server config", 
        action: "read, write, or delete",
        record: "optional: the record index to use" = None,
        payload: "optional: data to be written" = None) \
        -> "full curl cmd as string":
    '''
    Takes the server details, action, an optional record index and
    an optional data payload, and returns a full cURL command which
    is ready to be executed
    '''
    if action == "read":
        action = " -XGET "
    elif action == "write":
        action = " -POST "
    elif action == "delete":
        action = " -DELETE "
    else:
        raise ValueError(action, \
            " is an invalid action for migratorcfg.create_curl_cmd()")
    cmd = "curl -u " \
        + server_dict["user"] + ":" + server_dict["password"] \
        + action \
        + server_dict["server"] + ":" + server_dict["port"] \
        + "/".join(["", server_dict["index"], server_dict["type"], ""])
    if record is not None:
        cmd += record
    if payload is not None and action == " -POST ":
        cmd += " -H 'Content-Type: application/json' -d '\n" \
            + payload + "\n'"
    debug("migratorcfg:create_curl_cmd:", cmd)
    return cmd


def run_curl(cmd: "the cURL command to be executed") \
        -> "all output from the command":
    '''
    Takes a cURL command and executes it using subprocess.run with 
    these default parameters: 
        shell=True, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    '''
    debug("migratorcfg:run_curl: executing", cmd)
    returnval = subprocess.run(cmd, shell=True,\
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if "mapper_parsing_exception" in str(returnval) :
        raise ValueError("Elasticsearch returned a mapper_parsing_exception", returnval)
    else:
        return returnval
