本项目用于和开源的金融级区块链底层平台FISCO BCOS( https://www.github.com/fisco-bcos/ ) 建立JSONRPC协议的通信。支持版本为FISCO BCOS 2.0 RC1~RC3以及后续版本。

意图是构建一个代码尽量少，逻辑尽情轻，层级尽量浅，容易理解，可快速复用二次开发的python语言的客户端，所以命名内嵌了"lite"。

支持所有fisco bcos2.0 JSON RPC 接口，支持交易输入输出、event log等绝大部分的abi数据拼装和解析，支持直观的keystore账户管理(创建和加载等)，支持部署合约后保存最新地址和记录部署历史，基本上是一个简单而完整的fisco bcos 2.0客户端。

已经适配的python版本:python3.7.3

linux环境准备：

安装和使用，参见本目录下的 [linux_python_setup.md](./linux_python_setup.md)

熟悉pyenv和virutalenv的话应该比较顺利，也可以直接安装python3。强烈推荐多环境python设定。

安装pyenv和virtualenv完成后，参考命令：

	pyenv install 3.7.3 -v 

	pyenv rehash 

	pyenv virtualenv 3.7.3 blc
	
	pyenv activate blc

进入名为pytho 3.7.3 , blc的开发运行环境（blc这个名可替换）

----------------------------------------------------------------------------

windows环境准备：

1.安装python3.7.3 https://www.python.org/

2.安装virtualenv，使用文档： https://virtualenv.pypa.io/en/latest/userguide/

以下在windows的cmd环境工作

1.安装命令：pip install virtualenv

2.建立一个工作目录，如d:\python_env,进入d:\python_env

3.创建一个独立的python环境: virtualenv blc  ("blc"为环境名，可用其他名字)

4.运行：blc\Scripts\activate.bat

可以看到命令行前面多了（blc），独立的名为blc的python环境建立完成

----------------------------------------------------------------------------


获取项目代码：

	git clone https://github.com/coderkentzhang/bcosliteclientpy.git
	
目前代码在dev分支,建议在dev状态下运行体验，进行二次开发。

依次运行：

	git checkout dev
	
	cd bcosliteclient
	
	pip install -e .[dev]

安装依赖库(依赖库定义见setup.py文件)。

将client_config.py.template复制为client_config.py，或者直接将template后缀去掉。修改client_config.py里的值：

    remote_rpcurl="http://127.0.0.1:8545" #节点的rpc端口
	
    contract_info_file="bin/accounts/contract.ini" #保存已部署合约信息的文件
	
    account_keyfile_path="bin/accounts" #默认保存keystore文件的路径，在此路径下,keystore文件以 [name].keystore命名
	
    account_keyfile ="pyaccount.keystore" #默认的账号文件，用于交易签名
	
    account_password ="123456" #默认的账号文件的密码*使用时建议另外创建
	
    fiscoChainId=1
	
    groupid = 1
	
修改配置后，运行体验

clientdemo.py会加载默认演示合约sample/SimpleInfo.sol以及其abi,bin，进行部署，接口调用，解析返回信息等。可以参考clientdemo.py，编写其他逻辑。

	python clientdemo.py

***如报告Crypto包不存在，进入virtualenv的目录如d:\python_env\blc\lib\site-packages\,将小写的crypto目录名第一个字母改为大写Crypto （这貌似是windows环境的一个坑 ***

----------------------------------------------------------------------------

clientdemo.py演示调用client/bcosclient.py里实现的接口，已经实现fisco bcos的所有rpc查询接口（截止2019.06 FISCO BCOS 2.0rc3版本）

实现的发送交易接口为：

    deploy：部署合约

    call： 调用合约接口，返回只读的数据

    sendRawTransaction：返回transactionHash

    sendRawTransactionGetReceipt : 发送交易后等待共识完成，检索receipt，

sendRawTransaction这两个方法可用于所有已知abi的合约，传入abi定义，方法名，正确的参数列表，即可发送交易。交易由BcosClient里加载的账号进行签名。


解析数据采用datatypes/datatypeparse.py里实现的DatatypeParser对象的方法。


主要方法有：

    parse_transaction_input: 用于transaction，用于查询交易后解析input数据（方法+参数）

    parse_receipt_output： 用于receipt，解析合约接口的返回值

    parse_event_logs：用于receipt，解析eventlog数组，增加eventname，eventdata两个数据



此项目源自开源，回馈开源，其中eth-abi，eth-account，eth-hash，eth-keys，eth-typing，eth-utils，rlp, eth-rlp等都为开源项目，各子目录都保留了license,README，向原作者（们）致谢！
(是的，兼容evm，复用了abi/rlp编码，但底层项目实际上整个架构已经重写)


以上引用的代码有修订，为了便于修改，所以将这些项目并入代码目录，不采用发布包的方式引用。


本工程从开始准备到本文档完成历时五天，在工作之余的碎片时间和深夜完成，感谢开源社区既有代码的基础以及python语言的开发效率,所写代码不多，主要是发掘可用api和进行整理、重构、胶水式组合封装(准备和整理环境的时间，简直比写关键代码耗时还长:P)。欢迎体验和pr,一起持续更新维护。
