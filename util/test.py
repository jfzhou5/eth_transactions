from eth_account import Account
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider

from Eth_transaction.settings import ABI, CONTRACT_ADDRESS

web3 = Web3(HTTPProvider("http://localhost:7545"))
# for i in web3.eth.accounts:
#     print(i,type(i))
# 0xdaff18874cbc0291ecd94da92641f2fb0eddbb49 print(web3.toWei(1,'ether'))
# print(web3.isAddress('0x212861F610183429E275cE3E9aF26Dd0cE9bC4d8'))

action = web3.eth.contract(address=web3.toChecksumAddress(CONTRACT_ADDRESS), abi=ABI)

# print(web3.eth.coinbase)
# nonce = web3.eth.getTransactionCount(web3.toChecksumAddress("0x212861f610183429e275ce3e9af26dd0ce9bc4d8"))
# txn_dict = action.functions.add_ipo(1, 100000000, 12).buildTransaction({
#     'nonce': nonce,
#     "from": web3.toChecksumAddress("0x212861f610183429e275ce3e9af26dd0ce9bc4d8"),
# })
# signed_txn = web3.eth.account.signTransaction(txn_dict,
#                                               private_key="422f5a66ceb118d88fa8be2a972dcdefd2ada36e92d7cdec7404701e8b58c0d6")
# result_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

# print(action.functions.get_stock_price(60008).call())
#
nonce = web3.eth.getTransactionCount(web3.toChecksumAddress("0x212861f610183429e275ce3e9af26dd0ce9bc4d8"))
txn_dict = action.functions.buy(60008, 11, 10000000).buildTransaction({
    'value': web3.toWei(1, 'ether'),
    'nonce': nonce,
    "from": web3.toChecksumAddress("0x212861f610183429e275ce3e9af26dd0ce9bc4d8"),
})
signed_txn = web3.eth.account.signTransaction(txn_dict,
                                              private_key="422f5a66ceb118d88fa8be2a972dcdefd2ada36e92d7cdec7404701e8b58c0d6")
result_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
print(action.functions.get_id_counts().call())
# buys_index = action.functions.get_buys_index().call()
# print(f"buys_index:{buys_index}")
# for i in range(buys_index):
#     print(action.functions.get_buys(i).call())

# account = Account.privateKeyToAccount("17721ff8f59fcf139a2a1ff4062d7e075fbb03e90756d1aa02102504b3626e6d")
# print('private => {0}'.format(account._key_obj))
# print('public  => {0}'.format(account._key_obj.public_key))
# print('address => {0}'.format(account.address))
#
# ac = Account.create()

# print('private => {0}'.format(ac._key_obj))
# print('public  => {0}'.format(ac._key_obj.public_key))
# print('address => {0}'.format(ac.address))
# print(type(ac._key_obj))
# print(type(ac.address))
# print(web3.eth.getBalance(web3.toChecksumAddress('0x212861F610183429E275cE3E9aF26Dd0cE9bC4d8'), 'latest'))

