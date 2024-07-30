from web3 import Web3
from helper import Helper


'''
this file is created to have a helper class that will be used to interact with the blockchain
using web3.py library

like making the transactions and getting the contract instances

so that our server file does not get cluttered with the web3.py code
and only focus on data and streaming logic 

'''


class Web3Helper:
    def __init__(self) -> None:
        self.helper = Helper()
        self.conf = self.helper.conf
        self.web3 = Web3(Web3.HTTPProvider(self.helper.conf.RPC_URL))
        self.airvault_contract = self.web3.eth.contract(address=self.helper.conf.AIRVAULT_ADDRESS, abi=self.helper.conf.AIRVAULT_ABI)
        self.wintoken_contract = self.web3.eth.contract(address=self.helper.conf.WINTOKEN_ADDRESS, abi=self.helper.conf.WINTOKEN_ABI)
        self.account = self.web3.eth.account.from_key(self.conf.PRIVATE_KEY)
    
    def mint_win_tokens(self, user, win_tokens_amt):
       # Mint and distribute WIN tokens
        tx = self.wintoken_contract.functions.mint(user, win_tokens_amt).build_transaction({
            'chainId': self.conf.CHAINID,  # Assuming you are using Ganache, otherwise change this
            'gas': 2000000,
            'gasPrice': self.web3.to_wei('1', 'gwei'),
            'nonce': self.web3.eth.get_transaction_count(self.account.address),
        })
        signed_tx = self.web3.eth.account.sign_transaction(tx, private_key=self.conf.PRIVATE_KEY)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return self.web3.eth.wait_for_transaction_receipt(tx_hash)
        
        
    
        


