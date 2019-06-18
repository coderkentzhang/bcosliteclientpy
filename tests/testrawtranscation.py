from eth_account.account import (
    Account
)
from eth_utils.hexadecimal import decode_hex,encode_hex
from eth_account._utils.bcostransactions import BcosTransaction
from eth_account._utils.bcostransactions import(
    serializable_unsigned_transaction_from_dict,
    encode_transaction,
    is_int_or_prefixed_hexstr,
)
from collections import (
    Mapping,
)
import rlp

from  utils.abi import filter_by_name
import json
from utils.abi import *
from eth_utils.hexadecimal import decode_hex
from eth_abi import encode_single, encode_abi,decode_single
from utils.contracts import (
    prepare_transaction,
    encode_transaction_data,
)
import json
keyfile ="d:/blockchain/accounts/pyaccount.keystore"

#从keystore打开一个公私钥对
with open(keyfile, "r") as dump_f:
    keytext = json.load(dump_f)
    privkey = Account.decrypt(keytext,"123456")
    ac2 = Account.from_key(privkey)
    print("read from file: address",ac2.address)
    print("pubkey: ",ac2.publickey)
    print("privkey: ",encode_hex(ac2.key) )

'''
    #也可以从私钥文本得到一个可用来签名的帐户对象
    ac3 = Account.from_key("255f01b066a90853a0aa18565653d7b944cd2048c03613a9ff31cb9df9e693e5")
    print("test from key")
    print("read from file: address", ac3.address)
    print("pubkey: ", ac3.publickey)
    print("privkey: ", encode_hex(ac3.key))
'''
#从abi文件获得abi的文本定义
with open("sample\AddrTableWorker.abi", 'r') as load_f:
    contract_abi = json.load(load_f)
#将要调用的函数和参数编码
inputparams = ('abcefg', 1000, '0x7029c502b4F824d19Bd7921E9cb74Ef92392FB1b')
#第三个参数是方法的abi，可以传入None，encode_transaction_data做了修改，支持通过方法+参数在整个abi里找到对应的方法abi来编码
functiondata = encode_transaction_data("create",contract_abi,None,inputparams)
print("encode_transaction_data:",functiondata)
#填写一个bcos transaction 的 mapping
contractAddress= "0x7029c502b4F824d19Bd7921E9cb74Ef92392FB1b"
txmap =dict()
txmap["randomid"] = 500999 #测试用 todo:改为随机数
txmap["gasPrice"] = 30000000
txmap["gasLimit"] = 30000000
txmap["blockLimit"] = 101 #测试用，todo：从链上查一下
txmap["to"] = contractAddress
txmap["value"] = 0
txmap["data"] = functiondata
txmap["fiscoChainId"] = 1
txmap["groupId"] = 1
txmap["extraData"] = ""
#txmap["chainId"]=None #chainId没用了，fiscoChainId有用
print(txmap)
#将mapping构建一个transaction对象
transaction = serializable_unsigned_transaction_from_dict(txmap)
#感受下transaction encode的原始数据
print(encode_hex(rlp.encode(transaction)) )

#实际上只需要用sign_transaction就可以获得rawTransaction的编码数据了,input :txmap,私钥
signedTxResult = Account.sign_transaction(txmap,ac2.privateKey)
print(signedTxResult )
#signedTxResult.rawTransaction是二进制的，要放到rpc接口里要encode下
print(encode_hex(signedTxResult.rawTransaction) )


if True:
    import utils.rpc
    url = "http://119.29.114.153:8545"
    rpc = utils.rpc.HTTPProvider(url)
    param = [1,encode_hex(signedTxResult.rawTransaction)]
    #发送
    response = rpc.make_request("sendRawTransaction",param)
    print(response)