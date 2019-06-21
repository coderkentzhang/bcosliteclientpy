from client_config import client_config
from configobj import  ConfigObj

class ContractNote:
    @staticmethod
    def get_last(name):
        config = ConfigObj(client_config.contract_info_file, encoding='UTF8')
        if name in config["address"]:
            address = config["address"][name]
        else:
            address = None
        return address

    @staticmethod
    def save_address(contractname, newaddress, blocknum=None, memo=None):
        from configobj import ConfigObj
        import time
        #write to file
        config = ConfigObj(client_config.contract_info_file,
                           encoding='UTF8')
        if "addess" not in config:
            config['address']={}
        config['address'][contractname] = newaddress
        print (config)
        if blocknum!=None:
            if "history" not in config:
                config["history"]={}
            timestr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime());
            detail="{}:{},block:{}".format(contractname,timestr,blocknum)
            if memo !=None: #
                detail="{},{}".format(detail,memo)
            config["history"][newaddress] = detail
        config.write()
