from eth_account.account import (
    Account
)
from eth_utils.hexadecimal import decode_hex,encode_hex
import json
keyfile ="d:/blockchain/accounts/pyaccount.keystore"


with open(keyfile, "r") as dump_f:
    keytext = json.load(dump_f)
    privkey = Account.decrypt(keytext,"123456")
    ac2 = Account.from_key(privkey)
    print("read from file: address",ac2.address)
    print("privkey: ",encode_hex(ac2.key) )
    print("pubkey: ",ac2.publickey)