from client.bcosclient import (
    BcosClient,
    BcosError
)
from eth_utils import to_checksum_address
from  datatypes import datatype_parser
from  datatypes.datatype_parser import DatatypeParser
import json
client = BcosClient()
info = client.init()
print(info)
doQueryTest =False
if doQueryTest:
    print("\n>>---------------------------------------------------------------------")
    res = client.getClientVersion()
    print("\n>>---------------------------------------------------------------------")
    print("getClientVersion",res)
    print("\n>>---------------------------------------------------------------------")
    try:
        res = client.getBlockNumber()
        print("getBlockNumber",res)
    except BcosError as e:
        print("bcos client error,",e.info())
    print("\n>>---------------------------------------------------------------------")
    print("getPeers",client.getPeers())
    print("\n>>---------------------------------------------------------------------")
    print("getBlockByNumber",client.getBlockByNumber(50))
    print("\n>>---------------------------------------------------------------------")
    print("getBlockHashByNumber",client.getBlockHashByNumber(50))
    print("\n>>---------------------------------------------------------------------")
    print("getBlockByHash",client.getBlockByHash("0xe7588bf4ee5a6fb5aae9bdcc2c4f3c58cf7a789b15a4daa6617ed594b5ba3951"))
    print("\n>>---------------------------------------------------------------------")
    print("getTransactionByHash",client.getTransactionByHash("0x41fa9a0ce36d486ee2bf6d2219b68b44ca300ec7aeb07f8f2aa9c225655d2b61"))
    print("\n>>---------------------------------------------------------------------")
    print("getTransactionByBlockHashAndIndex",client.getTransactionByBlockHashAndIndex("0xe7588bf4ee5a6fb5aae9bdcc2c4f3c58cf7a789b15a4daa6617ed594b5ba3951",0))
    print("\n>>---------------------------------------------------------------------")
    print("getTransactionByBlockNumberAndIndex",client.getTransactionByBlockNumberAndIndex(50,0))
    print("\n>>---------------------------------------------------------------------")
    print("getTransactionReceipt",client.getTransactionReceipt("0x41fa9a0ce36d486ee2bf6d2219b68b44ca300ec7aeb07f8f2aa9c225655d2b61"))
    print("\n>>---------------------------------------------------------------------")
    print("getPendingTransactions",client.getPendingTransactions())
    print("\n>>---------------------------------------------------------------------")
    print("getPendingTxSize",client.getPendingTxSize())
    print("\n>>---------------------------------------------------------------------")
    print("getCode",client.getCode("0x83592a3cf1af302612756b8687c8dc7935c0ad1d"))
    print("\n>>---------------------------------------------------------------------")
    print("getTotalTransactionCount",client.getTotalTransactionCount())
    print("\n>>---------------------------------------------------------------------")
    print("getSystemConfigByKey",client.getSystemConfigByKey("tx_count_limit"))
    print("\n>>---------------------------------------------------------------------")

    print("getPbftView",int(client.getPbftView(),16))
    print("\n>>---------------------------------------------------------------------")
    print("getSealerList",client.getSealerList())
    print("\n>>---------------------------------------------------------------------")
    print("getObserverList",client.getObserverList())
    print("\n>>---------------------------------------------------------------------")
    print("getConsensusStatus",client.getConsensusStatus())
    print("\n>>---------------------------------------------------------------------")
    print("getSyncStatus",client.getSyncStatus())
    print("\n>>---------------------------------------------------------------------")
    print("getGroupPeers",client.getGroupPeers())
    print("\n>>---------------------------------------------------------------------")
    print("getNodeIDList",client.getNodeIDList())
    print("\n>>---------------------------------------------------------------------")
    print("getGroupList",client.getGroupList())

to_address = "0x09d88e27711e78d2c389eb8f532ccdc9abe43077"

#从文件加载abi文本定义
contractFile  ="sample\SimpleInfo.abi"
with open(contractFile, 'r') as load_f:
    contract_abi = json.load(load_f)
    load_f.close()
abimaven = DatatypeParser()
abimaven.set_abi(contract_abi)

print("\n>>Deploy:---------------------------------------------------------------------")
with open("sample\SimpleInfo.bin", 'r') as load_f:
    contract_bin = load_f.read()
    load_f.close()
result = client.deploy(contract_bin)
print("deploy",result)


print("\n>>sendRawTransaction:---------------------------------------------------------------------")
to_address = result['contractAddress'] #use new deploy address
args = ['simplename', 2024, to_checksum_address('0x7029c502b4F824d19Bd7921E9cb74Ef92392FB1c')]
result = client.sendRawTransactionGetReceipt(to_address,contract_abi,"set",args)
print(result)
logresult = abimaven.parse_event_logs(result["logs"])
print("parse log ")
for log in logresult:
    if 'eventname' in log:
        print("log name: {} , data: {}".format(log['eventname'],log['eventdata']))

txhash = result['transactionHash']
txresponse = client.getTransactionByHash(txhash)
inputresult = abimaven.parse_transaction_input(txresponse['input'])
print("transaction input parse:",txhash)
print(inputresult)



print("\n>>Call:---------------------------------------------------------------------")

res = client.call(to_address,contract_abi,"getbalance")
print("call",res)

