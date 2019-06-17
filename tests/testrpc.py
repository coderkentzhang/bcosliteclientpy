import sys
print (sys.path)
import utils.rpc
from  utils.abi import filter_by_name
import json
from utils.abi import *
from eth_utils.hexadecimal import decode_hex
url = "http://119.29.114.153:8545"
rpc = utils.rpc.HTTPProvider(url)
rpc.isConnected()
param=[1]

bn = rpc.make_request("getBlockNumber",param)
if "error" in bn:
    print("error %d, [%s]"%(bn["error"]["code"],bn["error"]["message"]))
else:
    print( int(bn['result'],16) )


txhash = "0x27a7e7c14470a534cbf491310d85ad8e5620a893637cc47cfac964413bb08bf9";
tx = rpc.make_request("getTransactionByHash",[1,txhash])
inputs  = tx["result"]["input"]
print (inputs)
with open("sample\AddrTableWorker.abi", 'r') as load_f:
    contract_abi = json.load(load_f)
print(contract_abi)
funcbyname = filter_by_name("create",contract_abi)

print(funcbyname[0]['inputs'])

from eth_utils import *

b4 = function_abi_to_4byte_selector(funcbyname[0])
print (encode_hex(b4))
b4_1 = abi_to_signature(funcbyname[0])
print(b4_1)
print(get_abi_input_types(funcbyname[0]))

functionhash = inputs[0:10]
params = inputs[10:]
print("functionhash :%s,inputs %s"%(functionhash,params) )
hexparams =decode_hex( params)
print(hexparams)
from eth_abi import encode_single, encode_abi,decode_single
abitext="(string,uint256,address)"
result = decode_single(abitext,hexparams);
print("decode result ",result)
encoderesult = encode_single(abitext,result);
print(encode_hex(encoderesult))
print('0x%s'%params)



'''
def prepare_transaction(
        address,
        fn_identifier,
        contract_abi=None,
        fn_abi=None,
        transaction=None,
        fn_args=None,
        fn_kwargs=None):'''
from utils.contracts import prepare_transaction
txpre = prepare_transaction(address = "0x7029c502b4f824d19bd7921e9cb74ef92392fb1b",
                    fn_identifier = "create",
                    contract_abi = contract_abi,
                    fn_args=('abc',1000,'0x7029c502b4F824d19Bd7921E9cb74Ef92392FB1b'),
                    transaction={'from': "0x8f62b0a6d7d928df18b1e86b8d76f7160519a9da",
                                 'gas':300000000,
                                 'gasPrice':300000000,
                                 'bocklimit':100
                                 }
                    )

print(txpre)
print(int('0x11e1a300',16))