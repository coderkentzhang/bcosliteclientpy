#!python
import argparse
import sys
import time
from client.stattool import StatTool
from configobj import ConfigObj
from client_config import client_config
from eth_account.account import (
    Account
)
from eth_utils.hexadecimal import encode_hex
from client.bcosclient import (
    BcosClient
)
from client.contractnote import ContractNote
import json
import os
from client.datatype_parser import DatatypeParser
from eth_utils import to_checksum_address

parser = argparse.ArgumentParser(description='FISCO BCOS 2.0 lite client @python')   # 首先创建一个ArgumentParser对象
parser.add_argument('cmd',    nargs="+" ,       # 添加参数
                    help='the command for console')
usagemsg = []
args = parser.parse_args()
print("user input : ",args.cmd)
cmd = args.cmd[0]
inputparams = args.cmd[1:]

usagemsg.append("newaccount [name] [password] : \ncreate a new account ,save to :[{}],(default) , the path spec in client_config.py:[account_keyfile_path]".format(client_config.account_keyfile_path))
if cmd == 'newaccount' :
    name=inputparams[0]
    password=inputparams[1]
    print ("starting : {} {} {} ".format(name,name,password))
    ac = Account.create(password)
    print("new address : ",ac.address)
    stat = StatTool.begin()
    kf = Account.encrypt(ac.privateKey, password)
    stat.done()
    print("encrypt use time : {}ms".format(stat.timeused))
    import json
    keyfile = "{}/{}.keystore".format(client_config.account_keyfile_path,name)
    print("save to file : [{}]".format(keyfile) )
    with open(keyfile, "w") as dump_f:
        json.dump(kf, dump_f)

    with open(keyfile, "r") as dump_f:
        keytext = json.load(dump_f)
        stat = StatTool.begin()
        privkey = Account.decrypt(keytext,password)
        stat.end()
        print("decrypt use time : {}ms".format(stat.timeused))
        ac2 = Account.from_key(privkey)
        print("-------------->>")

        print("address:",ac2.address)
        print("privkey:",encode_hex(ac2.key))
        print("pubkey :",ac2.publickey)
        print("\naccount store in file: [{}]".format(keyfile))
        print("\n**** please remember your password !!! *****")

def default_abi_file(contractname):
    abi_file = contractname
    if not abi_file.endswith(".abi"): #default from sample/xxxx.abi,if only input a name
        abi_file = "sample/" + contractname + ".abi"
    return abi_file



def fill_params(params,paramsname):
    index = 0
    result=dict()
    for name in paramsname:
        result[name]=params[index]
        index+=1
    return result
client = BcosClient ()

def print_receipt_logs_and_txoutput(receipt,contractname,parser=None):
    print("\n>>  receipt logs : ")
    # 解析receipt里的log
    if parser == None and len(contractname) > 0:
        parser = DatatypeParser(default_abi_file(contractname))
    logresult = parser.parse_event_logs(receipt["logs"])
    i = 0
    for log in logresult:
        if 'eventname' in log:
            i = i + 1
            print("{}): log name: {} , data: {}".format(i, log['eventname'], log['eventdata']))
    txhash = receipt["transactionHash"]
    txresponse = client.getTransactionByHash(txhash)
    inputdetail = print_parse_transaction(txresponse, "", parser)
    # 解析该交易在receipt里输出的output,即交易调用的方法的return值
    outputresult = parser.parse_receipt_output(inputdetail['name'], receipt['output'])
    print("receipt output :", outputresult)

def format_args_by_abi(inputparams,inputabi):
    paramformatted = []
    index=-1
    #print(inputabi)
    #print(inputparams)
    for input in inputabi:
        #print(input)
        index +=1
        param = inputparams[index]
        if '\'' in param:
            param = param.replace('\'',"")
        if "int" in input["type"]:
            paramformatted.append(int(param,10))
            continue
        #print(input)
        if "address" in input["type"]:
            print ("to checksum address ",param)
            paramformatted.append(to_checksum_address(param))
            continue
        paramformatted.append(param)
    print("param formatted by abi:",paramformatted)
    return paramformatted

def format_args_by_types(inputparams,types):
    index = -1;
    newparam=[]
    #print(types)
    for type in types:
        index += 1
        v = inputparams[index]
        if type=="str":
            if '\'' in v:
                v = v.replace('\'','')
            newparam.append(v)
            continue
        if type=="hex":
            newparam.append(hex(int(v,10)))
            continue
        if type=="bool":
            if v.lower()=="true":
                newparam.append(True)
            else:
                newparam.append(False)

            continue
    #print(newparam)
    return newparam


def print_parse_transaction(tx,contractname,parser=None):
    if parser == None:
        parser = DatatypeParser(default_abi_file(contractname) )
    inputdata = tx["input"]
    inputdetail = parser.parse_transaction_input(inputdata)
    print(">> transaction hash : ", tx["hash"])
    print("tx input data detail:\n {}".format(inputdetail))
    return (inputdetail)


#---------------------------------------------------------------------------
#start command functions




usagemsg.append("deploy [abi binary file] save\ndeploy contract from a binary file,if 'save' spec, so save addres to file")
if cmd=="deploy":
    '''deploy abi bin file'''
    abibinfile=inputparams[0]
    with open(abibinfile,"r") as f:
        contractbin = f.read()
    result = client.deploy(contractbin)
    print ("deploy result  for [{}] is:\n {}".format(abibinfile,json.dumps(result,indent=4) ))
    name = contractname = os.path.splitext(os.path.basename(abibinfile))[0]
    address = result['contractAddress']
    blocknum = int(result["blockNumber"],16)
    print("on block : {},address: {} ".format(blocknum,address))
    if len(inputparams) == 2:
        if inputparams[1]=="save":
            ContractNote.save_address(name, address, blocknum)
            print("address save to file: ",client_config.contract_info_file)
    else:
        print("\nNOTE : if want to save new address as last addres for (call/sendtx)\nadd 'save' to cmdline and run again")
    sys.exit(0)

usagemsg.append('''call [contractname] [address] [func]  [args...] 
eg: call SimpleInfo 0xF2c07c98a6829aE61F3cB40c69f6b2f035dD63FC getbalance1 11
if address is "last" ,then load last address from :{}
eg: call SimpleInfo last getall
'''.format(client_config.contract_info_file))
if cmd=="call":
    paramsname = ["contractname", "address", "func"]
    params = fill_params(inputparams,paramsname)
    args = inputparams[len(paramsname):]
    contractname = params["contractname"]
    data_parser = DatatypeParser(default_abi_file(contractname))
    contract_abi = data_parser.contract_abi

    address = params["address"]
    if address=="last":
        address = ContractNote.get_last(contractname)
        if address == None:
            sys.exit("can not get last address for [{}],break;".format(contractname))
    funcname =params["func"]
    inputabi = data_parser.func_abi_map_by_name[funcname]["inputs"]
    args = format_args_by_abi(args,inputabi)
    print ("call {} , address: {}, func: {}, args:{}"
           .format(contractname,address,funcname,args))
    result = client.call(address,contract_abi,funcname,args)
    print("call result: ",result )


usagemsg.append('''sendtx [contractname]  [address] [func] [args...] 
eg: sendtx SimpleInfo 0xF2c07c98a6829aE61F3cB40c69f6b2f035dD63FC set 'test' 100 '0xF2c07c98a6829aE61F3cB40c69f6b2f035dD63FC'
if address is "last" ,then load last address from :{}
eg: sendtx SimpleInfo last set 'test' 100 '0xF2c07c98a6829aE61F3cB40c69f6b2f035dD63FC'
'''.format(client_config.contract_info_file))
if cmd=="sendtx":
    paramsname = ["contractname", "address", "func"]
    params = fill_params(inputparams,paramsname)
    args = inputparams[len(paramsname):]
    contractname = params["contractname"]
    data_parser = DatatypeParser(default_abi_file(contractname))
    contract_abi = data_parser.contract_abi

    address = params["address"]
    if address=="last":
        address = ContractNote.get_last(contractname)
        if address == None:
            sys.exit("\ncan not get last address for [{}],break;\n".format(contractname))

    funcname = params["func"]
   # print("data_parser.func_abi_map_by_name",data_parser.func_abi_map_by_name)
    inputabi = data_parser.func_abi_map_by_name[funcname]["inputs"]
    args = format_args_by_abi(args,inputabi)
    #from eth_utils import to_checksum_address
    #args = ['simplename', 2024, to_checksum_address('0x7029c502b4F824d19Bd7921E9cb74Ef92392FB1c')]
    print ("sendtx {} , address: {}, func: {}, args:{}"
           .format(contractname,address,funcname,args))
    receipt = client.sendRawTransactionGetReceipt(address,contract_abi,params["func"],args)
    print("\n\nsendtx receipt: ",json.dumps(receipt,indent=4) )
    #解析receipt里的log 和 相关的tx ,output
    print_receipt_logs_and_txoutput(receipt,"",data_parser)




getcmds=dict()
getcmds["getClientVersion"]=[]
getcmds["getBlockNumber"]=[]
getcmds["getPbftView"]=[]
getcmds["getSealerList"]=[]
getcmds["getObserverList"]=[]
getcmds["getConsensusStatus"]=[]
getcmds["getSyncStatus"]=[]
getcmds["getPeers"]=[]
getcmds["getGroupPeers"]=[]
getcmds["getNodeIDList"]=[]
getcmds["getGroupList"]=[]
getcmds["getBlockByHash"]=["str","bool"]
getcmds["getBlockByNumber"]=["hex","bool"]
getcmds["getBlockHashByNumber"]=["hex"]
getcmds["getTransactionByHash"]=["str"]
getcmds["getTransactionByBlockHashAndIndex"]=["str","hex"]
getcmds["getTransactionByBlockNumberAndIndex"]=["hex","hex"]
getcmds["getTransactionReceipt"]=["str"]
getcmds["getPendingTransactions"]=[]
getcmds["getPendingTxSize"]=[]
getcmds["getCode"]=["str"]
getcmds["getTotalTransactionCount"]=[]
getcmds["getSystemConfigByKey"]=["str"]





usagemsg.append('''all the 'get' command for JSON RPC\neg: [getBlockyByNumber 10].
use 'list' cmd to show all getcmds ''')
if cmd in getcmds:
    types = getcmds[cmd]
    fmtparams = format_args_by_types(inputparams, types)
    print("is a get :{},params:{}".format(cmd,fmtparams) )
    params = [client.groupid]
    params.extend(fmtparams)
    #print(params)
    result  = client.common_request(cmd,params)
    print(json.dumps(result,indent=4))
    if cmd == "getTransactionReceipt":
        if len(inputparams) == 2:
            contractname = inputparams[1]

            print_receipt_logs_and_txoutput(result,contractname)


    if "getBlock" in cmd:
        blocknum = int(result["number"],16)
        print(">> blocknumber : ",blocknum)
        print(">> blockhash   : ", result["hash"])
    if "getTransactionBy" in cmd :
        #print(inputparams)
        abifile=None
        if len(inputparams) == 3:
            abifile = inputparams[2]
        if len(inputparams) == 2 and cmd == "getTransactionByHash":
            abifile = inputparams[1]
        if abifile!=None:
            print_parse_transaction(result,abifile)


usagemsg.append("list: list all getcmds (getBlock...getTransaction...getReceipt..getOthers)")
if cmd == "list":
    print("query commands:")
    for cmd in getcmds:
        print ("{} : {}".format(cmd,getcmds[cmd]))


usagemsg.append("int [hexnum]: convert a hex str to int ,eg: int 0x65")
if cmd == 'int':
    print(int(inputparams[0],16))


usagemsg.append('''txinput [abifile] [inputdata(inhex)]
parse the transaction input data by spec abifile，eg: txinput sample/SimpleInfo.abi [txinputdata]''')
if cmd =="txinput":
    contractname = inputparams[0]
    inputdata = inputparams[1]

    dataParser = DatatypeParser(default_abi_file(contractname) )
    #print(dataParser.func_abi_map_by_selector)
    result = dataParser.parse_transaction_input(inputdata)
    print("\nabifile : ",default_abi_file(contractname))
    print("parse result: {}".format(result))


usagemsg.append('''checkaddr [address]: change address to checksum address according EIP55:
to_checksum_address: 0xf2c07c98a6829ae61f3cb40c69f6b2f035dd63fc -> 0xF2c07c98a6829aE61F3cB40c69f6b2f035dD63FC
''')
if cmd == "checkaddr":

    address = inputparams[0]
    result = to_checksum_address(address)
    print("to_checksum_address:")
    print("{} -->\n{}".format(address,result) )


if cmd == "usage":
    print("usage of console (FISCO BCOS 2.0 lite client @python):")
    index = 0
    for msg in usagemsg:
        index+=1
        print("\n{}): {}".format(index,msg) )