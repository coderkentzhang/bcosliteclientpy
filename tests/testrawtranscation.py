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


with open(keyfile, "r") as dump_f:
    keytext = json.load(dump_f)
    privkey = Account.decrypt(keytext,"123456")
    ac2 = Account.from_key(privkey)
    print("read from file: address",ac2.address)
    print("pubkey: ",ac2.publickey)
    print("privkey: ",encode_hex(ac2.key) )

with open("sample\AddrTableWorker.abi", 'r') as load_f:
    contract_abi = json.load(load_f)
inputparams = ('abcefg', 1000, '0x7029c502b4F824d19Bd7921E9cb74Ef92392FB1b')
functiondata = encode_transaction_data("create",contract_abi,None,inputparams)
print("encode_transaction_data:",functiondata)

'''
ac3 = Account.from_key("255f01b066a90853a0aa18565653d7b944cd2048c03613a9ff31cb9df9e693e5")
print("test from key")
print("read from file: address", ac3.address)
print("pubkey: ", ac3.publickey)
print("privkey: ", encode_hex(ac3.key))
'''

txmap =dict()
txmap["randomid"] = 50099
txmap["gasPrice"] = 30000000
txmap["gasLimit"] = 30000000
txmap["blockLimit"] = 101
txmap["to"] = "0x7029c502b4F824d19Bd7921E9cb74Ef92392FB1b"
txmap["value"] = 0
txmap["data"] = functiondata
txmap["fiscoChainId"] = 1
txmap["groupId"] = 1
txmap["extraData"] = ""
#txmap["chainId"]=None
'''
tx =  BcosTransaction(
randomid = 500,
gasPrice = 30000000,
gasLimit = 30000000,
blockLimit = 501,
to = "",
value = 0,
data = "abcdefg",
fiscoChainId = 1,
groupId = 1,
extraData = "",
r=None,
s=None,
v=None
)
'''


print(txmap)
print("is_int_or_prefixed_hexstr",txmap["randomid"],is_int_or_prefixed_hexstr(txmap["randomid"]) )
encoderesult = serializable_unsigned_transaction_from_dict(txmap)
print(encode_hex(rlp.encode(encoderesult)) )
signResult = Account.sign_transaction(txmap,ac2.privateKey)
print(signResult )
print(encode_hex(signResult.rawTransaction) )


if True:
    import utils.rpc
    url = "http://119.29.114.153:8545"
    rpc = utils.rpc.HTTPProvider(url)
    param = [1,encode_hex(signResult.rawTransaction)]
    response = rpc.make_request("sendRawTransaction",param)
    print(response)