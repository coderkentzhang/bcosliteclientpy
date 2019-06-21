#!python
import argparse
from configobj import ConfigObj
from client_config import client_config
from eth_account.account import (
    Account
)
from eth_utils.hexadecimal import encode_hex
from client.bcosclient import (
    BcosClient
)
import json
import os
from client.datatype_parser import DatatypeParser

parser = argparse.ArgumentParser(description='FISCO BCOS 2.0 lite client @python')   # 首先创建一个ArgumentParser对象
parser.add_argument('cmd',    nargs="+" ,       # 添加参数
                    help='the command for console')
usagemsg = []
args = parser.parse_args()
print("user input : ",args.cmd)
cmd = args.cmd[0]
inputparams = args.cmd[1:]

usagemsg.append("newaccount [name] [password] : \ncreate a new account ,save to :[{}],(default) or the path spec in client_config.py:[account_keyfile_path]".format(client_config.account_keyfile_path))
if cmd == 'newaccount' :
    name=inputparams[0]
    password=inputparams[1]
    print ("starting : {} {} {} ".format(name,name,password))
    ac = Account.create(password)
    print("new address : ",ac.address)
    kf = Account.encrypt(ac.privateKey, password)
    import json
    keyfile = "{}/{}.keystore".format(client_config.account_keyfile_path,name)
    print("save to file : [{}]".format(keyfile) )
    with open(keyfile, "w") as dump_f:
        json.dump(kf, dump_f)

    with open(keyfile, "r") as dump_f:
        keytext = json.load(dump_f)
        privkey = Account.decrypt(keytext,password)
        ac2 = Account.from_key(privkey)
        print("-------------->>")

        print("address:",ac2.address)
        print("privkey:",encode_hex(ac2.key))
        print("pubkey :",ac2.publickey)
        print("\naccount store in file: [{}]".format(keyfile))
        print("\n**** please remember your password !!! *****")

def fill_params(params,paramsname):
    index = 0
    result=dict()
    for name in paramsname:
        result[name]=params[index]
        index+=1
    return result
client = BcosClient ()

def print_receipt_logs(receipt,parser):
    # 解析receipt里的log
    logresult = parser.parse_event_logs(receipt["logs"])
    i = 0
    for log in logresult:
        if 'eventname' in log:
            i = i + 1
            print("{}): log name: {} , data: {}".format(i, log['eventname'], log['eventdata']))


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
        paramformatted.append(param)
    print("paramformatted:",paramformatted)
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
            if v.lower=="true":
                newparam.append(True)
            else:
                newparam.append(False)
            continue
    #print(newparam)
    return newparam




data_parser = DatatypeParser()

usagemsg.append("deploy [abi binary file]\ndeploy contract from a binary file")
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
    #client.save_contract_address( name,address,blocknum )

usagemsg.append('''call [contractname] [address] [func]  [args...] 
eg: call SimpleInfo 0xF2c07c98a6829aE61F3cB40c69f6b2f035dD63FC getbalance1 11
if address is "ini" ,then load address from :{}
**importance: for args, use '' for str or address ,eg: 'test','0xF2c07c98a6829aE61F3cB40c69f6b2f035dD63FC'
'''.format(client_config.contract_info_file))
if cmd=="call":
    paramsname = ["contractname", "address", "func"]
    params = fill_params(inputparams,paramsname)
    args = inputparams[len(paramsname):]
    abi_file="{}/{}.abi".format("sample",params["contractname"])
    data_parser = DatatypeParser()
    data_parser.load_abi_file(abi_file)
    contract_abi = data_parser.contract_abi
    address = params["address"]
    if address=="ini":
        config = ConfigObj(client_config.contract_info_file,encoding='UTF8')
        address = config["address"][params["contractname"]]
    funcname =params["func"]
    inputabi = data_parser.func_abi_map_by_name[funcname]["inputs"]
    args = format_args_by_abi(args,inputabi)
    print ("call {} , address: {}, func: {}, args:{}"
           .format(params["contractname"],address,funcname,args))
    result = client.call(address,contract_abi,funcname,args)
    print("call result: ",result )


usagemsg.append('''sendtx [contractname]  [address] [func] [args...] 
eg: sendtx SimpleInfo 0xF2c07c98a6829aE61F3cB40c69f6b2f035dD63FC set 'test' 100 '0xF2c07c98a6829aE61F3cB40c69f6b2f035dD63FC'
if address is "ini" ,then load address from :{}
**importance: for args, use '' for str or address ,eg: 'test','0xF2c07c98a6829aE61F3cB40c69f6b2f035dD63FC'
'''.format(client_config.contract_info_file))
if cmd=="sendtx":
    paramsname = ["contractname", "address", "func"]
    params = fill_params(inputparams,paramsname)
    args = inputparams[len(paramsname):]
    abi_file="{}/{}.abi".format("sample",params["contractname"])
    data_parser = DatatypeParser()
    data_parser.load_abi_file(abi_file)
    contract_abi = data_parser.contract_abi
    address = params["address"]
    if address=="ini":
        config = ConfigObj(client_config.contract_info_file,encoding='UTF8')
        address = config["address"][params["contractname"]]
    funcname = params["func"]
   # print("data_parser.func_abi_map_by_name",data_parser.func_abi_map_by_name)
    inputabi = data_parser.func_abi_map_by_name[funcname]["inputs"]
    args = format_args_by_abi(args,inputabi)
    #from eth_utils import to_checksum_address
    #args = ['simplename', 2024, to_checksum_address('0x7029c502b4F824d19Bd7921E9cb74Ef92392FB1c')]
    print ("sendtx {} , address: {}, func: {}, args:{}"
           .format(params["contractname"],address,funcname,args))
    receipt = client.sendRawTransactionGetReceipt(address,contract_abi,params["func"],args)
    print("\n\nsendtx receipt: ",json.dumps(receipt,indent=4) )
    #解析receipt里的log
    print("\n>>parse receipt and transaction:----------------------------------------------------------")
    txhash = receipt['transactionHash']
    print("transaction hash: " ,txhash)
    print_receipt_logs(receipt,data_parser)
    txresponse = client.getTransactionByHash(txhash)
    inputresult = data_parser.parse_transaction_input(txresponse['input'])
    print("transaction input parse:",txhash)
    print(inputresult)

    #解析该交易在receipt里输出的output,即交易调用的方法的return值
    outputresult  = data_parser.parse_receipt_output(inputresult['name'], receipt['output'])
    print("receipt output :",outputresult)



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
        print(inputparams)
        if len(inputparams) == 2:
            parser = DatatypeParser()
            parser.load_abi_file(inputparams[1])
            print("receipt  logs :")
            print_receipt_logs(result,parser)
    if "getBlock" in cmd:
        blocknum = int(result["number"],16)
        print(">> blocknumber : ",blocknum)
        print(">> blockhash   : ", result["hash"])
    if "getTransaction" in cmd:
        #print(inputparams)
        if len(inputparams) == 2:
            parser = DatatypeParser()
            parser.load_abi_file(inputparams[1])
            inputdata = result["input"]
            result = parser.parse_transaction_input(inputdata)
            print("\nabifile : ", inputparams[1])
            print("transaction input parse result:\n {}".format(result))


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
    abifilename = inputparams[0]
    inputdata = inputparams[1]

    dataParser = DatatypeParser()
    dataParser.load_abi_file(abifilename)

    #print(dataParser.func_abi_map_by_selector)
    result = dataParser.parse_transaction_input(inputdata)
    print("\nabifile : ",abifilename)
    print("parse result: {}".format(result))


usagemsg.append('''checkaddr [address]: change address to checksum address according EIP55:
to_checksum_address: 0xf2c07c98a6829ae61f3cb40c69f6b2f035dd63fc -> 0xF2c07c98a6829aE61F3cB40c69f6b2f035dD63FC
''')
if cmd == "checkaddr":
    from eth_utils import  to_checksum_address
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