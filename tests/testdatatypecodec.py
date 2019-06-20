from datatypes import datatype_parser
from datatypes.datatype_parser import DatatypeParser

import json

if(True):
    abimaven = DatatypeParser()
    abimaven.load_abi_file("sample/SimpleInfo.abi")
    abimaven.parse_abi()

    with open("sample/receipt.json","r") as f :
        receipt = json.load(f)
        f.close()
    logs = receipt["logs"]
    abimaven.parse_event_logs(logs)
    print("parse result")
    for log in logs:
        print(log)

if True:
    abimaven = DatatypeParser()
    abimaven.load_abi_file("sample/SimpleInfo.abi")
    abimaven.parse_abi()
    with open("sample/tx_simpleinfo_set.json","r") as f :
        tx = json.load(f)
        f.close()
    result = abimaven.parse_transaction_input(tx["input"])
    print(result)