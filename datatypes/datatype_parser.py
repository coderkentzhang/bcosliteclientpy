#codec for abi,block,transaction,receipt,logs
import json
from eth_abi import(
    encode_single,
    encode_abi,
    decode_single,
    decode_abi
    )
from eth_utils.abi import (
    collapse_if_tuple,
)
from eth_utils import (
    function_signature_to_4byte_selector,
    event_abi_to_log_topic,
    encode_hex,decode_hex)

from utils.abi import  (
    filter_by_type,
    abi_to_signature,
    get_abi_output_types,
    get_fn_abi_types,
    get_fn_abi_types_str,
    exclude_indexed_event_inputs,
    exclude_indexed_event_inputs_to_array,
    exclude_indexed_event_inputs_to_str,
    data_tree_map)

class DatatypeParser:
    contract_abi = None
    func_abi_map_by_selector = dict()
    func_abi_map_by_name = dict()
    event_abi_map = dict()
    def __init__(self):
        pass
    def from_text(self,abitext):
        self.contract_abi = json.loads(abitext)
        self.parse_abi()

    def set_abi(self,abi):
        self.contract_abi = abi
        self.parse_abi()

    def load_abi_file(self,abi_file):

        with open(abi_file, 'r') as load_f:
            self.contract_abi = json.load(load_f)
            load_f.close()
            self.parse_abi()



    def parse_abi(self):
        '''for item in self.contract_abi:
            if (item["type"] != "constructor"):
                print(item["name"], " is a ", item["type"])
                hash4 = function_signature_to_4byte_selector(item["name"] + '()')
                print("function hash4:", encode_hex(hash4))'''
        funclist = filter_by_type("function",self.contract_abi)
        for func in funclist:
            signature = abi_to_signature(func)
            selector = function_signature_to_4byte_selector(signature)
            #print(func)
            #print(signature)
            #print(encode_hex(selector) )
            self.func_abi_map_by_selector[encode_hex(selector)] = func
            self.func_abi_map_by_name[func['name']]= func

        eventlist = filter_by_type("event",self.contract_abi)
        for event in eventlist:
            topic = event_abi_to_log_topic(event)
            #print(event)
            #print(encode_hex(topic) )
            self.event_abi_map[encode_hex(topic)] = event

    #用于receipt，解析eventlog数组，在原数据中增加解析后的 eventname，eventdata两个数据
    def parse_event_logs(self,logs):
        #print(self.event_abi_map)
        for log in logs:
            if(len(log["topics"]) == 0 ):#匿名event
                continue
            topic = log["topics"][0]
            if topic not in self.event_abi_map:
                continue
            eventabi = self.event_abi_map[topic]
            #print(eventabi)
            if(eventabi == None):
                continue
            #args_abi = get_fn_abi_types(eventabi,'inputs')
            argslist = exclude_indexed_event_inputs_to_str(eventabi)
            #print(argslist)
            result = decode_single(argslist,decode_hex(log['data']))
            #print(result)
            log["eventdata"] = result
            log["eventname"] = eventabi["name"]
        return logs

    #用于transaction，用于查询交易后解析input数据（方法+参数）
    #返回 result['name'] result['args']
    def parse_transaction_input(self,inputdata):
        selector = inputdata[0:10]
        argsdata = inputdata[10:]
        #print(selector)
        #print(self.func_abi_map_by_selector.keys())
        if selector not in self.func_abi_map_by_selector:
            return None
        func_abi = self.func_abi_map_by_selector[selector]
        #print(func_abi)
        args_abi = get_fn_abi_types_str(func_abi,"inputs")
        args = decode_single(args_abi,decode_hex(argsdata) )
        result= dict()
        result['name'] = func_abi["name"]
        result['args'] = args
        return result

    # 用于receipt，解析合约接口的返回值
    # 取决于接口定义
    def parse_receipt_output(self,name,outputdata):
        if name not in self.func_abi_map_by_name:
            return None
        func_abi = self.func_abi_map_by_name[name]
        output_args = get_fn_abi_types_str(func_abi,"outputs")
        #print(output_args)
        result = decode_single(output_args,decode_hex(outputdata) )
        return result



