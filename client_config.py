#- * - coding: utf - 8 -
class client_config:
#类成员变量，便于用.调用和区分命名空间
    remote_rpcurl="http://119.29.114.153:8545" #节点的rpc端口
    contract_info_file="sample/contract.ini" #保存已部署合约信息的文件
    account_keyfile_path="d:/blockchain/accounts" #保存keystore文件的路径，在此路径下,keystore文件以 [name].keystore命名
    account_keyfile ="pyaccount.keystore"
    account_password ="123456"
    fiscoChainId=1
    groupid = 1

