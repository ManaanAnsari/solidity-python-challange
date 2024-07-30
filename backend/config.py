import os
from dotenv import load_dotenv
import json

load_dotenv()

'''
this config class mainly exists to keep all the configurations in one place

i recommend setting all the config in the .env file and then loading them here

'''

class Config:
    def __init__(self) -> None:
        self.CACHE_FILE=os.getenv('CACHE_FILE')
        self.EVENTS_FILE=os.getenv('EVENTS_FILE')
        self.PRIVATE_KEY=str(os.getenv('PRIVATE_KEY'))
        self.RPC_URL=os.getenv('RPC_URL')
        self.CHAINID=int(os.getenv('CHAINID'))
        self.AIRVAULT_ADDRESS=os.getenv('AIRVAULT_ADDRESS')
        self.WINTOKEN_ADDRESS=os.getenv("WINTOKEN_ADDRESS")
        self.X=int(os.getenv("X"))
        if os.path.isfile(os.getenv("AIRVAULT_ABI")):
            with open(os.getenv("AIRVAULT_ABI"), 'r') as f:
                airvault_data = json.load(f)
                self.AIRVAULT_ABI = airvault_data["abi"]
        else:
            raise Exception("AIRVAULT_ABI configuration missing")
        
        if os.path.isfile(os.getenv("WINTOKEN_ABI")):
            with open(os.getenv("WINTOKEN_ABI"), 'r') as f:
                wintoken_data = json.load(f)
                self.WINTOKEN_ABI = wintoken_data["abi"]
        else:
            raise Exception("WINTOKEN_ABI configuration missing")
        
    

